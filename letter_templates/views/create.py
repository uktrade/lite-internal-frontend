from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form

from core.builtins.custom_tags import get_string
from letter_templates import helpers
from letter_templates.forms import add_letter_template
from letter_templates.helpers import get_template_content
from letter_templates.services import get_letter_paragraphs, post_letter_template
from letter_templates.views.letter_paragraphs import get_order_paragraphs_page


class Add(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, add_letter_template().forms[0])

    def post(self, request):
        response = submit_paged_form(request, add_letter_template(), post_letter_template)[0]

        if response:
            return response

        template_content = get_template_content(request)
        return get_order_paragraphs_page(request, template_content)


class Preview(TemplateView):
    def post(self, request):
        template_content = get_template_content(request)
        letter_paragraphs = get_letter_paragraphs(request, template_content['letter_paragraphs'])
        preview = helpers.generate_preview(template_content['layout'], letter_paragraphs)

        return render(request, 'letter_templates/preview.html', {
            'preview': preview,
            'name': template_content['name'],
            'layout': template_content['layout'],
            'restricted_to': template_content['restricted_to'],
            'letter_paragraphs': template_content['letter_paragraphs']
        })


class Create(TemplateView):
    def post(self, request):
        letter_paragraphs = request.POST.getlist('letter_paragraphs')
        post_letter_template(request, request.POST, letter_paragraphs)
        messages.success(request, get_string('letter_templates.letter_templates.successfully_created_banner'))
        return redirect('letter_templates:letter_templates')
