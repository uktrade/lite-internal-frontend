from django import template
from django.template import engines

from markdown import Markdown


register = template.Library()


@register.simple_tag(takes_context=True)
def markdown_to_html(context):
    """
    Template tag to render the html and replace
    placeholder tags with user requested params
    """

    # Convert markdown text to html
    md = Markdown()
    text = md.convert(context.get('content', ''))
    if not text:
        return ''

    # Do string substitution for placeholders
    django_engine = engines['django']
    page = django_engine.from_string(text)

    text = page.render(context.flatten())

    return text
