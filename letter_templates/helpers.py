import os

from django.template import Engine, Context

from conf import settings


def template_engine_factory():
    """
    Create a template engine configured for use with letter templates.
    """
    return Engine(
        string_if_invalid='{{ %s }}',
        dirs=[os.path.join(settings.LETTER_TEMPLATES_DIRECTORY)],
        libraries={'sass_tags': 'sass_processor.templatetags.sass_tags'}
    )


def generate_preview(layout, letter_paragraphs: list):
    django_engine = template_engine_factory()

    template = django_engine.get_template(f'{layout}.html')

    letter_context = Context({
        'content': '<br><br>'.join([paragraph['text'] for paragraph in letter_paragraphs])
    })
    return template.render(letter_context)


def get_template_content(request):
    data = request.POST.copy()
    return {
        "name": data.get('name'),
        "layout": data.get('layout'),
        "restricted_to": data.getlist('restricted_to'),
        "action": data.get('action'),
        "letter_paragraphs": data.getlist('letter_paragraphs')
    }
