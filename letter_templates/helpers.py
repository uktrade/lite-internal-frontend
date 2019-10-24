import os

from django.template import Engine, Context

from conf import settings


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
