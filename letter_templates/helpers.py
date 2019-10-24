import os

from django.shortcuts import render
from django.template import Engine, Context

from conf import settings
from letter_templates.services import get_letter_paragraphs


def generate_preview(layout, letter_paragraphs: list):
    django_engine = Engine(
        string_if_invalid='{{ %s }}',
        dirs=[os.path.join(settings.LETTER_TEMPLATES_DIRECTORY)],
        libraries={'sass_tags': 'sass_processor.templatetags.sass_tags'}
    )

    template = django_engine.get_template(f'{layout}.html')

    letter_context = Context({
        'content': '<br><br>'.join([paragraph['text'] for paragraph in letter_paragraphs])
    })
    return template.render(letter_context)


def generate_generator(request, letter_paragraphs, name, layout, restricted_to):
    letter_paragraphs = get_letter_paragraphs(request, letter_paragraphs)
    return render(request, 'letter_templates/generator.html', {'letter_paragraphs': letter_paragraphs,
                                                               'name': name,
                                                               'layout': layout,
                                                               'restricted_to': restricted_to})
