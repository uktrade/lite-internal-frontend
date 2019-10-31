from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
from lite_forms.generators import error_page, form_page
from lite_forms.submitters import submit_paged_form

from core.builtins.custom_tags import get_string
from letter_templates.forms import add_letter_template
from letter_templates.helpers import get_template_content
from letter_templates.services import post_letter_template
from letter_templates.views.letter_paragraphs import get_order_paragraphs_page


class Add(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, add_letter_template().forms[0])

    @staticmethod
    def post(request):
        response, _ = submit_paged_form(request,
                                        add_letter_template(),
                                        post_letter_template,
                                        expect_many_values=["restricted_to"])

        if response:
            return response

        template_content = get_template_content(request)
        return get_order_paragraphs_page(request, template_content)


class Create(TemplateView):
    @staticmethod
    def post(request):
        json = request.POST.copy()
        json['letter_paragraphs'] = request.POST.getlist('letter_paragraphs')
        json['restricted_to'] = request.POST.getlist('restricted_to')

        response, status = post_letter_template(request, json)

        if 200 <= status < 300:
            messages.success(request, get_string('letter_templates.letter_templates.successfully_created_banner'))
            return redirect('letter_templates:letter_templates')

        else:
            error_messages = []
            errors = response["errors"]
            for field, field_errors in errors.items():
                for field_error in field_errors:
                    error_messages.append(field_error)

            return error_page(None, "; ".join(error_messages))
