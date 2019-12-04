from http import HTTPStatus

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from cases.forms.generate_document import select_template_form, edit_document_text_form, add_paragraphs_form
from cases.services import post_generated_document, get_generated_document_preview
from core.helpers import convert_dict_to_query_params
from letter_templates.services import get_letter_templates, get_letter_template
from lite_content.lite_internal_frontend.cases import GenerateDocumentsPage
from lite_forms.generators import form_page, error_page
from lite_forms.views import SingleFormView
from picklists.services import get_picklists


class SelectTemplate(TemplateView):
    def get(self, request, **kwargs):
        params = {"case": str(kwargs["pk"])}
        templates = get_letter_templates(request, convert_dict_to_query_params(params))
        return form_page(request, select_template_form(templates, str(kwargs["pk"])))

    def post(self, request, **kwargs):
        template_id = request.POST.get("template")
        if template_id:
            return redirect(
                reverse_lazy("cases:generate_document_edit", kwargs={"pk": str(kwargs["pk"]), "tpk": template_id})
            )
        else:
            return redirect(reverse_lazy("cases:generate_document", kwargs={"pk": str(kwargs["pk"])}))


class EditDocumentText(SingleFormView):
    @staticmethod
    def _validate_text(request, json):
        json["text"] = "\n\n".join(json["text"])
        return json, HTTPStatus.OK

    def init(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        template_id = str(kwargs["tpk"])
        keys = {"pk": case_id, "tpk": template_id}

        if "text" not in request.POST:
            paragraph_text = get_letter_template(
                request, template_id, params=convert_dict_to_query_params({"text": True})
            )[0]["text"]
            self.data = {"text": paragraph_text}

        self.form = edit_document_text_form(case_id, keys)
        self.redirect = False
        self.action = self._validate_text


class AddDocumentParagraphs(SingleFormView):
    @staticmethod
    def _validate_text(request, json):
        return json, HTTPStatus.OK

    def init(self, request, **kwargs):
        letter_paragraphs = get_picklists(request, "letter_paragraph")["picklist_items"]
        case_id = str(kwargs["pk"])
        template_id = str(kwargs["tpk"])

        self.form = add_paragraphs_form(letter_paragraphs, request.POST["text"], {"pk": case_id, "tpk": template_id})
        self.redirect = False
        self.action = self._validate_text


def _error_page():
    return error_page(
        None, title=GenerateDocumentsPage.TITLE, description=GenerateDocumentsPage.ERROR, show_back_link=True,
    )


class PreviewDocument(TemplateView):
    def post(self, request, pk, tpk):
        template_id = str(tpk)
        case_id = str(pk)

        # Redirect to add paragraphs instead if button is clicked
        if "add_paragraphs" in request.POST:
            kwargs = {"tpk": template_id, "pk": case_id, "text": request.POST["text"]}
            return redirect(reverse_lazy("cases:generate_document_add_paragraphs", kwargs=kwargs))

        if "text" in request.POST:
            text = request.POST["text"]
        else:
            return _error_page()

        preview, status_code = get_generated_document_preview(request, case_id, template_id, text=text)
        if status_code == 400:
            return _error_page()

        return render(
            request,
            "generated_documents/preview.html",
            {"preview": preview["preview"], "text": text, "pk": case_id, "tpk": template_id},
        )


class CreateDocument(TemplateView):
    def post(self, request, **kwargs):
        if "text" not in request.POST:
            return _error_page()
        text = request.POST["text"]
        template_id = str(kwargs["tpk"])
        case_id = str(kwargs["pk"])
        post_generated_document(request, case_id, {"template": template_id, "text": text})
        return redirect(reverse_lazy("cases:documents", kwargs={"pk": case_id}))
