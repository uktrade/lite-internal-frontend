from http import HTTPStatus

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from cases.forms.generate_document import select_template_form, edit_document_text_form, select_addressee_form
from cases.helpers.helpers import generate_document_error_page
from cases.services import (
    post_generated_document,
    get_generated_document_preview,
    get_generated_document,
    get_case,
    get_case_additional_contacts,
    get_case_applicant,
)
from core.helpers import convert_dict_to_query_params
from letter_templates.services import get_letter_template
from lite_forms.components import FormGroup
from lite_forms.views import SingleFormView, MultiFormView

TEXT = "text"
TEMPLATE = "template"


class GenerateDocument(MultiFormView):
    contacts: []
    applicant: {}
    template: str

    @staticmethod
    def _validate(request, pk, json):
        return json, HTTPStatus.OK

    def get_forms(self):
        if self.contacts:
            return FormGroup(
                [
                    select_template_form(self.request, self.kwargs, back_url="cases:case"),
                    select_addressee_form(),
                    edit_document_text_form(self.kwargs, self.template, post_url="cases:generate_document_preview"),
                ]
            )
        else:
            return FormGroup(
                [
                    select_template_form(self.request, self.kwargs, back_url="cases:case"),
                    edit_document_text_form(self.kwargs, self.template, post_url="cases:generate_document_preview"),
                ]
            )

    def init(self, request, **kwargs):
        self.contacts = get_case_additional_contacts(request, kwargs["pk"])
        self.applicant = get_case_applicant(request, kwargs["pk"])
        self.template = request.POST.get(TEMPLATE)

        if self.template and not request.POST.get(TEXT):
            template, _ = get_letter_template(request, self.template, params=convert_dict_to_query_params({TEXT: True}))
            self.data = {TEXT: template[TEXT]}

        self.object_pk = kwargs["pk"]
        self.action = self._validate
        self.additional_context = {
            "case": get_case(request, self.object_pk),
            "applicant": self.applicant,
            "contacts": self.contacts,
        }


class GenerateDecisionDocument(GenerateDocument):
    def get_forms(self):
        return FormGroup(
            [
                select_template_form(self.request, self.kwargs, back_url="cases:finalise_documents"),
                edit_document_text_form(self.kwargs, self.template, post_url="cases:finalise_document_preview"),
            ]
        )


class RegenerateExistingDocument(SingleFormView):
    def init(self, request, **kwargs):
        document, status_code = get_generated_document(request, str(kwargs["pk"]), str(kwargs["dpk"]))
        template = document["template"]
        self.object_pk = kwargs["pk"]
        self.form = edit_document_text_form(kwargs, template, post_url="cases:generate_document_preview")
        self.success_url = reverse_lazy("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"]})
        self.context = {"case": get_case(request, self.object_pk)}


class PreviewDocument(TemplateView):
    def post(self, request, **kwargs):
        template_id = str(kwargs["tpk"])
        case_id = str(kwargs["pk"])

        text = request.POST.get(TEXT)
        if not text:
            return generate_document_error_page()

        preview, status_code = get_generated_document_preview(request, case_id, template_id, text=text)
        if status_code == 400:
            return generate_document_error_page()

        return render(
            request, "generated-documents/preview.html", {"preview": preview["preview"], TEXT: text, "kwargs": kwargs},
        )


class CreateDocument(TemplateView):
    def post(self, request, queue_pk, pk, tpk):
        text = request.POST.get(TEXT)
        if not text:
            return generate_document_error_page()

        status_code = post_generated_document(
            request, str(pk), {"template": str(tpk), TEXT: text, "visible_to_exporter": True}
        )
        if status_code != HTTPStatus.CREATED:
            return generate_document_error_page()
        else:
            return redirect(
                reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": str(pk), "tab": "documents"})
            )


class CreateDocumentFinalAdvice(TemplateView):
    def post(self, request, queue_pk, pk, decision_key, tpk):
        text = request.POST.get(TEXT)
        if not text:
            return generate_document_error_page()

        status_code = post_generated_document(
            request,
            str(pk),
            {"template": str(tpk), TEXT: text, "visible_to_exporter": False, "advice_type": decision_key},
        )
        if status_code != HTTPStatus.CREATED:
            return generate_document_error_page()
        else:
            return redirect(reverse_lazy("cases:finalise_documents", kwargs={"queue_pk": queue_pk, "pk": pk}))
