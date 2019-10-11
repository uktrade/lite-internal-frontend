import os

from django.template import engines

from conf import settings


def generate_preview(layout, letter_paragraphs: list):
    django_engine = engines['django']
    template = django_engine.from_string(
        open(os.path.join(settings.LETTER_TEMPLATES_DIRECTORY, f'{layout}.html'), 'r').read())

    letter_context = {
        'content': '\n\n'.join([x['text'] for x in letter_paragraphs]),
    }
    return template.render(letter_context)
