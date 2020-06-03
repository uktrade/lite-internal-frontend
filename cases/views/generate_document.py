from http import HTTPStatus
from urllib.parse import quote

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
from letter_templates.services import get_letter_template, get_letter_templates
from lite_forms.components import FormGroup
from lite_forms.views import SingleFormView, MultiFormView

TEXT = "text"
TEMPLATE = "template"


class GenerateDocument(MultiFormView):
    contacts: []
    applicant: {}
    template: str
    back_url: str

    @staticmethod
    def _validate(request, pk, json):
        return json, HTTPStatus.OK

    def get_forms(self):
        params = {"case": self.kwargs["pk"], "page": self.request.GET.get("page", 1)}
        templates, _ = get_letter_templates(self.request, convert_dict_to_query_params(params))

        if self.contacts:
            return FormGroup(
                [
                    select_template_form(templates, self.back_url),
                    select_addressee_form(self.back_url),
                    edit_document_text_form(
                        {"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"], "tpk": self.template},
                        post_url="cases:generate_document_preview",
                        back_url=self.back_url,
                    ),
                ]
            )
        else:
            return FormGroup(
                [
                    select_template_form(templates, self.back_url),
                    edit_document_text_form(
                        {"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"], "tpk": self.template},
                        post_url="cases:generate_document_preview",
                        back_url=self.back_url,
                    ),
                ]
            )

    def init(self, request, **kwargs):
        self.back_url = reverse_lazy(
            "cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"], "tab": "documents"}
        )
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
        self.back_url = reverse_lazy(
            "cases:finalise_documents", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]}
        )
        params = {
            "case": self.kwargs["pk"],
            "decision": self.kwargs["decision_key"],
            "page": self.request.GET.get("page", 1),
        }
        templates, _ = get_letter_templates(self.request, convert_dict_to_query_params(params))

        return FormGroup(
            [
                select_template_form(templates, back_url=self.back_url),
                edit_document_text_form(
                    {
                        "queue_pk": self.kwargs["queue_pk"],
                        "pk": self.kwargs["pk"],
                        "tpk": self.template,
                        "decision_key": self.kwargs["decision_key"],
                    },
                    post_url="cases:finalise_document_preview",
                    back_url=self.back_url,
                ),
            ]
        )


class RegenerateExistingDocument(SingleFormView):
    def init(self, request, **kwargs):
        back_url = reverse_lazy(
            "cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"], "tab": "documents"}
        )
        document, status_code = get_generated_document(request, str(kwargs["pk"]), str(kwargs["dpk"]))
        template = document["template"]
        self.data = {TEXT: document.get(TEXT)}
        self.object_pk = kwargs["pk"]
        self.form = edit_document_text_form(
            {"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"], "tpk": template},
            post_url="cases:generate_document_preview",
            back_url=back_url,
        )
        self.context = {"case": get_case(request, self.object_pk)}


class PreviewDocument(TemplateView):
    def post(self, request, **kwargs):
        template_id = str(kwargs["tpk"])
        case_id = str(kwargs["pk"])
        addressee = request.POST.get("addressee", "")

        text = request.POST.get(TEXT)
        if not text:
            return generate_document_error_page()

        params = convert_dict_to_query_params({"template": template_id, "text": quote(text), "addressee": addressee})
        preview, status_code = get_generated_document_preview(request, case_id, params)
        if status_code == 400:
            return generate_document_error_page()

        return render(
            request,
            "generated-documents/preview.html",
            {"preview": preview["preview"], TEXT: text, "addressee": addressee, "kwargs": kwargs},
        )


class CreateDocument(TemplateView):
    def post(self, request, queue_pk, pk, tpk):
        text = request.POST.get(TEXT)
        if not text:
            return generate_document_error_page()

        status_code = post_generated_document(
            request,
            str(pk),
            {"template": str(tpk), TEXT: text, "addressee": request.POST.get("addressee"), "visible_to_exporter": True},
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
