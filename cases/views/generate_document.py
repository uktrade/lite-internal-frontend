from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from cases.forms.generate_document import select_template_form
from letter_templates.services import get_letter_templates
from lite_forms.generators import form_page


class SelectTemplate(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, select_template_form(get_letter_templates(request)))

    def post(self, request, **kwargs):
        template_id = request.POST.get('template')
        if template_id:
            return redirect(reverse_lazy('cases:generate_document_preview',
                                         kwargs={'pk': str(kwargs["pk"]), 'tpk': template_id}))
        else:
            return redirect(reverse_lazy('cases:generate_document', kwargs={'pk': str(kwargs["pk"])}))


class PreviewDocument(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, select_template_form(get_letter_templates(request)))
