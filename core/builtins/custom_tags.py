from django import template
from django.template.defaultfilters import stringfilter

import datetime

register = template.Library()

ISO8601_FMT = '%Y-%m-%dT%H:%M:%SZ'


@register.filter
@stringfilter
def str_date(value):
    return datetime.datetime.strptime(value, ISO8601_FMT)
