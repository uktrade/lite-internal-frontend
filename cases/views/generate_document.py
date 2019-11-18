import uuid

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from weasyprint import HTML, CSS

from cases.forms.generate_document import select_template_form
from cases.services import get_case
from conf.settings import BASE_DIR
from letter_templates.helpers import generate_preview, paragraphs_to_markdown
from letter_templates.services import get_letter_templates, get_letter_template, get_letter_paragraphs
from lite_forms.generators import form_page


CSS_LOCATION = '/assets/css/styles.css'


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
        self.template = get_letter_template(request, self.template_id)
        self.case = get_case(request, self.case_id)
        self.content = {
            "content": paragraphs_to_markdown(get_letter_paragraphs(request, self.template["letter_paragraphs"])),
            "case": self.case,
        }
        self.preview = generate_preview(self.template["layout"]["filename"], self.content)
        return super(PreviewDocument, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return render(request, "generated_documents/preview.html",
                      {"preview": self.preview, "pk": self.case_id, "tpk": self.template_id})

    def post(self, request, **kwargs):
        html = HTML(string=self.preview)
        css = CSS(filename=BASE_DIR+CSS_LOCATION)
        html.write_pdf(f'/tmp/{uuid.uuid4()}.pdf', stylesheets=[css])
        return redirect(reverse_lazy("cases:case", kwargs={"pk": self.case_id}))
