import os

from django.shortcuts import render
from django.template import Engine, Context

from conf import settings
from letter_templates.services import get_letter_paragraphs


def generate_preview(layout, letter_paragraphs: list):
    django_engine = Engine(string_if_invalid='{{ %s }}')
    with open(os.path.join(settings.LETTER_TEMPLATES_DIRECTORY, f'{layout}.html'), 'r') as html_file:
        template = django_engine.from_string(html_file.read())

    letter_context = Context({
        'content': '<br><br>'.join([x['text'] for x in letter_paragraphs])
    })
    return template.render(letter_context)


def generate_generator(request, letter_paragraphs, name, layout, restricted_to):
    letter_paragraphs = get_letter_paragraphs(request, letter_paragraphs)
    return render(request, 'letter_templates/generator.html', {'letter_paragraphs': letter_paragraphs,
                                                               'name': name,
                                                               'layout': layout,
                                                               'restricted_to': restricted_to})
