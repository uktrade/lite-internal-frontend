from django.shortcuts import render
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form

from letter_templates.forms import add_letter_template


class LetterTemplates(TemplateView):

    def get(self, request, **kwargs):
        context = {

        }
        return render(request, 'letter_templates/letter_templates.html', context)


# Remove this!
def return_success(test, test2):
    return {'success': True}, True


class Add(TemplateView):

    def get(self, request, **kwargs):
        return form_page(request, add_letter_template().forms[0])

    def post(self, request, **kwargs):
        response, _ = submit_paged_form(request, add_letter_template(), return_success)

        if response:
            return response
