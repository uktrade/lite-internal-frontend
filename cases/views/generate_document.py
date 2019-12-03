from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from cases.forms.generate_document import select_template_form, edit_document_text_form
from cases.services import post_generated_document, get_generated_document_preview
from core.helpers import convert_dict_to_query_params
from letter_templates.services import get_letter_templates, get_letter_template
from lite_content.lite_internal_frontend.cases import GenerateDocumentsPage
from lite_forms.generators import form_page, error_page
from lite_forms.views import SingleFormView


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
    def init(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        template_id = str(kwargs["tpk"])
        paragraph_text = get_letter_template(
            request,
            template_id,
            params=convert_dict_to_query_params({"text": True})
        )[0]["text"]
        self.form = edit_document_text_form(case_id, {"pk": case_id, "tpk": template_id})
        self.data = {"text": paragraph_text}


class PreviewDocument(TemplateView):
    @staticmethod
    def _error_page():
        return error_page(
            None, title=GenerateDocumentsPage.TITLE, description=GenerateDocumentsPage.ERROR, show_back_link=True,
        )

    def post(self, request, **kwargs):
        template_id = str(kwargs["tpk"])
        case_id = str(kwargs["pk"])

        if "text" in request.POST:
            text = request.POST["text"]
        else:
            return self._error_page()

        preview, status_code = get_generated_document_preview(request, case_id, template_id, text=text)
        if status_code == 400:
            return self._error_page()

        return render(
            request,
            "generated_documents/preview.html",
            {"preview": preview["preview"], "pk": case_id, "tpk": template_id},
        )


class CreateDocument(TemplateView):
    def post(self, request, **kwargs):
        template_id = str(kwargs["tpk"])
        case_id = str(kwargs["pk"])
        post_generated_document(request, case_id, {"template": template_id})
        return redirect(reverse_lazy("cases:documents", kwargs={"pk": case_id}))
