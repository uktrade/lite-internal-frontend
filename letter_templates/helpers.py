import os

from django.template import engines

from conf import settings


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
