import os

from django.shortcuts import render
from django.template import engines
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form

from conf import settings
from letter_templates.forms import add_letter_template
from letter_templates.services import get_letter_paragraphs
from picklists.services import get_picklists


class LetterTemplates(TemplateView):

    def get(self, request, **kwargs):
        context = {
            'letter_templates': [
                {
                    'id': '123',
                    'name': 'I am a letter template',
                    'type': 'SIEL',
                    'last_modified_at': '12:03am Thursday 29 March 2019',
                },
                {
                    'id': '123',
                    'name': 'I am a letter template',
                    'type': 'SIEL',
                    'last_modified_at': '12:03am Thursday 29 March 2019',
                }
            ]
        }
        return render(request, 'letter_templates/letter_templates.html', context)


# Remove this!
def return_success(test, test2):
    return {'success': True}, True


def generate_preview(request, letter_paragraphs):
    django_engine = engines['django']
    template = django_engine.from_string(
        open(os.path.join(settings.LETTER_TEMPLATES_DIRECTORY, 'licence.html'), 'r').read())
    letter_context = {
        'content': request.POST.get('content', ''),
    }
    preview = template.render(letter_context)

    return render(request, 'letter_templates/generator.html', {'preview': preview,
                                                               'letter_paragraphs': letter_paragraphs})


class Add(TemplateView):

    def get(self, request, **kwargs):
        return form_page(request, add_letter_template().forms[0])

    def post(self, request, **kwargs):
        response, _ = submit_paged_form(request, add_letter_template(), return_success)

        if response:
            return response

        return generate_preview(request, [])


class LetterParagraphs(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        data = request.POST.copy()
        action = data.get('action')
        existing_letter_paragraphs = data.getlist('letter_paragraphs')

        if action == 'add_letter_paragraph':
            all_letter_paragraphs = get_picklists(request, 'letter_paragraph')
            context = {
                'letter_paragraphs': [x for x in all_letter_paragraphs['picklist_items'] if x['id'] not in existing_letter_paragraphs],
                'existing_letter_paragraphs': existing_letter_paragraphs
            }
            return render(request, 'letter_templates/letter_paragraphs.html', context)
        elif 'delete' in action:
            pk_to_delete = action.split('.')[1]
            existing_letter_paragraphs.remove(pk_to_delete)

        return generate_preview(request, letter_paragraphs=get_letter_paragraphs(request, existing_letter_paragraphs))


class Preview(TemplateView):

    def get(self, request, **kwargs):
        letter_paragraphs = get_picklists(request, 'letter_paragraph')
        return render(request, 'letter_templates/letter_paragraphs.html', {'letter_paragraphs': letter_paragraphs['picklist_items']})

    def post(self, request, **kwargs):
        django_engine = engines['django']
        template = django_engine.from_string(open(os.path.join(settings.LETTER_TEMPLATES_DIRECTORY, 'licence.html'), 'r').read())
        letter_context = {
            'content': request.POST.get('content', ''),
        }
        preview = template.render(letter_context)

        return render(request, 'letter_templates/generator.html', {'preview': preview})
