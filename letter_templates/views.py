from django.shortcuts import render
from django.views.generic import TemplateView
from lite_forms.generators import form_page

from letter_templates.forms import add_letter_template


class LetterTemplates(TemplateView):

    def get(self, request, **kwargs):
        context = {

        }
        return render(request, 'letter_templates/letter_templates.html', context)


class Add(TemplateView):

    def get(self, request, **kwargs):
        return form_page(request, add_letter_template().forms[0])
