from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from lite_forms.generators import error_page, form_page
from lite_forms.submitters import submit_paged_form

from letter_templates import helpers
from letter_templates.forms import add_letter_template
from letter_templates.services import get_letter_paragraphs, post_letter_templates
from picklists.services import get_picklists


class Add(TemplateView):

    def get(self, request, **kwargs):
        return form_page(request, add_letter_template().forms[0])

    def post(self, request, **kwargs):
        response, _ = submit_paged_form(request,
                                        add_letter_template(),
                                        post_letter_templates,
                                        expect_many_values=["restricted_to"])

        if response:
            return response

        return helpers.generate_generator(request,
                                          letter_paragraphs=[],
                                          name=request.POST.get('name'),
                                          layout=request.POST.get('layout'),
                                          restricted_to=request.POST.getlist('restricted_to'))


def get_template_content(request):
    data = request.POST.copy()
    return {
        "name": data.get('name'),
        "layout": data.get('layout'),
        "restricted_to": data.getlist('restricted_to'),
        "action": data.get('action'),
        "letter_paragraphs": data.getlist('letter_paragraphs')
    }


class LetterParagraphs(TemplateView):
    def post(self, request):
        template_content = get_template_content(request)
        if template_content['action'] == 'add_letter_paragraph':
            all_letter_paragraphs = get_picklists(request, 'letter_paragraph')
            context = {
                'name': template_content['name'],
                'layout': template_content['layout'],
                'restricted_to': template_content['restricted_to'],
                'letter_paragraphs': [x for x in all_letter_paragraphs['picklist_items'] if
                                      x['id'] not in template_content['letter_paragraphs']],
                'existing_letter_paragraphs': template_content['letter_paragraphs']
            }
            return render(request, 'letter_templates/letter_paragraphs.html', context)
        elif template_content['action'] == 'preview':
            return self._preview(request, template_content)
        elif 'delete' in template_content['action']:
            pk_to_delete = template_content['action'].split('.')[1]
            template_content['letter_paragraphs'].remove(pk_to_delete)

        return helpers.generate_generator(request,
                                          letter_paragraphs=template_content['letter_paragraphs'],
                                          name=template_content['name'],
                                          layout=template_content['layout'],
                                          restricted_to=template_content['restricted_to'])

    def _preview(self, request, template_content):
        """
        Display a preview once letter paragraphs have been selected and sorted.
        """
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
        letter_template_data = request.POST.copy()
        letter_template_data["letter_paragraphs"] = request.POST.getlist('letter_paragraphs')
        letter_template_data["restricted_to"] = request.POST.getlist('restricted_to')
        response, status = post_letter_templates(request, letter_template_data)

        if 200 <= status < 300:
            messages.success(request, 'The letter template was created successfully')
            return redirect('letter_templates:letter_templates')
        else:
            error_messages = []
            errors = response["errors"]
            for field, field_errors in errors.items():
                for field_error in field_errors:
                    error_messages.append(field_error)

            return error_page(None, "; ".join(error_messages))
