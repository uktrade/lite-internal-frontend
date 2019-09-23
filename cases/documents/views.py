import os
from collections import MutableMapping

from django.shortcuts import render, redirect
from django.template import engines
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from cases.documents.services import get_letter_templates
from cases.services import get_case
from conf import settings


class PickATemplate(TemplateView):

    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case = get_case(request, case_id)

        context = {
            'title': 'Flags',
            'case': case,
            'templates': get_letter_templates(request),
            'show_error': request.GET.get('show_error'),
        }
        return render(request, 'documents/select_a_template.html', context)


def flatten_data_new(d, parent_key='', sep='.'):
    """
    Flattens dictionaries eg
    {
        'site': {
            'name': 'SITE1'
            'address_line_1': '110 ...'
        }
    }
    becomes
    [
        'site.name',
        'site.address_line_1'
    ]
    """
    items = []

    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_data_new(v, new_key, sep=sep))
        else:
            items.append(new_key)

    return items


class CreateDocument(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        case_id = str(kwargs['pk'])
        case = get_case(request, case_id)
        template = request.GET.get('template')

        if not template:
            return redirect(reverse_lazy('cases:documents:pick_a_template', kwargs={'pk': case_id}) + '?show_error=True')

        django_engine = engines['django']
        template = django_engine.from_string(open(os.path.join(settings.LETTER_TEMPLATES_DIRECTORY, f'{template}.html'), 'r').read())
        letter_context = {
            'applicant': case.get('query').get('organisation'),
            'query': case.get('query'),
            'content': request.POST.get('content', ''),
        }
        preview = template.render(letter_context)

        context = {
            'title': 'Flags',
            'preview': preview,
            'content': letter_context.pop('content'),
            'letter_context': letter_context,
            'flattened_letter_context': flatten_data_new(letter_context)
        }
        return render(request, 'documents/document_generator.html', context)


class Help(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'documents/help.html')
