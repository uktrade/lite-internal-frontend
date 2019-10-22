import os

from django.shortcuts import render
from django.template import engines

from conf import settings
from letter_templates.services import get_letter_paragraphs


def generate_preview(layout, letter_paragraphs: list):
    django_engine = engines['django']
    template = django_engine.from_string(
        open(os.path.join(settings.LETTER_TEMPLATES_DIRECTORY, f'{layout}.html'), 'r').read())

    letter_context = {
        'content': '<br><br>'.join([x['text'] for x in letter_paragraphs]),
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


def generate_generator(request, letter_paragraphs, name, layout, restricted_to):
    letter_paragraphs = get_letter_paragraphs(request, letter_paragraphs)
    return render(request, 'letter_templates/generator.html', {'letter_paragraphs': letter_paragraphs,
                                                               'name': name,
                                                               'layout': layout,
                                                               'restricted_to': restricted_to})
