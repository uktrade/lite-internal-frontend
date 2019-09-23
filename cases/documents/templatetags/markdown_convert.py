from django import template
from django.utils.safestring import mark_safe
from django.template import engines

from markdown import Markdown


register = template.Library()


@register.simple_tag(takes_context=True)
def markdown_convert(context):
    """
    Template tag to render the html and replace
    placeholder tags with user requested params
    """

    # Convert markdown text to html
    md = Markdown()
    text = md.convert(context.get('content', ''))

    # Do string substitution for placeholders
    django_engine = engines['django']
    page = django_engine.from_string(text)

    if not text:
        return mark_safe('<p style="opacity: 0.6;">No content provided</p>')

    text = page.render(context.flatten())

    return mark_safe(text)
