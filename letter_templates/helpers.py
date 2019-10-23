import os

from django.shortcuts import render
from django.template import engines

from conf import settings
from letter_templates.services import get_letter_paragraphs


def sort_letter_paragraphs(paragraphs, ids):
    """Order a list of letter paragraphs in the same order as a list of IDs."""
    paragraphs_by_id = {p["id"]: p for p in paragraphs}
    return [paragraphs_by_id[id] for id in ids if id in paragraphs_by_id]


def generate_preview(layout, letter_paragraphs: list):
    django_engine = engines['django']
    template = django_engine.from_string(
        open(os.path.join(settings.LETTER_TEMPLATES_DIRECTORY, f'{layout}.html'), 'r').read())

    letter_context = {
        'content': '\n\n'.join([x['text'] for x in letter_paragraphs]),
        'applicant': {
            'name': '{{ applicant.name }}',
            'primary_site': {
                'address': {
                    'address_line_1': '{{ applicant.primary_site.address.address_line_1 }}',
                    'address_line_2': '{{ applicant.primary_site.address.address_line_2 }}',
                    'postcode': '{{ applicant.primary_site.address.postcode }}',
                    'city': '{{ applicant.primary_site.address.city }}',
                    'region': '{{ applicant.primary_site.address.region }}',
                    'country': {
                        'name': '{{ applicant.primary_site.address.country.name }}'
                    }
                }
            }
        }
    }
    return template.render(letter_context)


def generate_generator(request, letter_paragraph_ids, name, layout, restricted_to):
    letter_paragraphs = get_letter_paragraphs(request, letter_paragraph_ids)
    letter_paragraphs = sort_letter_paragraphs(letter_paragraphs,
                                               request.POST.getlist("letter_paragraphs"))
    return render(request, 'letter_templates/generator.html', {'letter_paragraphs': letter_paragraphs,
                                                               'name': name,
                                                               'layout': layout,
                                                               'restricted_to': restricted_to})
