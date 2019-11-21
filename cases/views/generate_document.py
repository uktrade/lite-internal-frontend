from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from cases.forms.generate_document import select_template_form
from cases.services import post_generated_document, get_generated_document_preview
from letter_templates.services import get_letter_templates
from lite_forms.generators import form_page

CSS_LOCATION = "/assets/css/styles.css"


class SelectTemplate(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, select_template_form(get_letter_templates(request)))

    def post(self, request, **kwargs):
        template_id = request.POST.get("template")
        if template_id:
            return redirect(
                reverse_lazy("cases:generate_document_preview", kwargs={"pk": str(kwargs["pk"]), "tpk": template_id})
            )
        else:
            return redirect(reverse_lazy("cases:generate_document", kwargs={"pk": str(kwargs["pk"])}))


class PreviewDocument(TemplateView):
    template_id: str
    case_id: str
    template: object
    case: object
    content: dict
    preview: str

    def dispatch(self, request, *args, **kwargs):
        self.template_id = str(kwargs["tpk"])
        self.case_id = str(kwargs["pk"])
        return super(PreviewDocument, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        preview = get_generated_document_preview(request, self.case_id, self.template_id)[0]["preview"]
        return render(
            request,
            "generated_documents/preview.html",
            {"preview": preview, "pk": self.case_id, "tpk": self.template_id},
        )

    def post(self, request, **kwargs):
        post_generated_document(request, self.case_id, {"template": self.template_id})
        return redirect(reverse_lazy("cases:documents", kwargs={"pk": self.case_id}))
