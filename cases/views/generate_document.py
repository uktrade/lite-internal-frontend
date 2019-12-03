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
    case_id: str
    template_id: str

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs["pk"])
        self.template_id = str(kwargs["tpk"])
        return super(EditDocumentText, self).dispatch(request, *args, **kwargs)

    def init(self, request, **kwargs):
        paragraph_text = get_letter_template(
            request,
            self.template_id,
            params=convert_dict_to_query_params({"text": True})
        )[0]["text"]
        self.form = edit_document_text_form(self.case_id)
        self.success_url = reverse_lazy("users:users")
        self.data = {"text": paragraph_text}

    def post(self, request, **kwargs):
        text = request.POST.get("text")
        kwargs = {"pk": self.case_id, "tpk": self.template_id}
        if text:
            return redirect(reverse_lazy("cases:generate_document_preview", kwargs=kwargs))
        else:
            return redirect(reverse_lazy("cases:generate_document_edit", kwargs=kwargs))


class PreviewDocument(TemplateView):
    template_id: str
    case_id: str
    template: object
    case: object
    content: dict
    preview: str

    @staticmethod
    def _error_page():
        return error_page(
            None, title=GenerateDocumentsPage.TITLE, description=GenerateDocumentsPage.ERROR, show_back_link=True,
        )

    def dispatch(self, request, *args, **kwargs):
        self.template_id = str(kwargs["tpk"])
        self.case_id = str(kwargs["pk"])
        return super(PreviewDocument, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        preview, status_code = get_generated_document_preview(request, self.case_id, self.template_id)
        if status_code == 400:
            return self._error_page()
        return render(
            request,
            "generated_documents/preview.html",
            {"preview": preview["preview"], "pk": self.case_id, "tpk": self.template_id},
        )

    def post(self, request, **kwargs):
        post_generated_document(request, self.case_id, {"template": self.template_id})
        return redirect(reverse_lazy("cases:documents", kwargs={"pk": self.case_id}))
