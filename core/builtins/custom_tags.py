import datetime
import json
import warnings

import stringcase
from django import template
from django.template.defaultfilters import stringfilter
from django.templatetags.tz import do_timezone
from django.utils.safestring import mark_safe

from conf.constants import ISO8601_FMT
from conf.settings import env
from core import lite_strings

from lite_content.lite_internal_frontend import strings

register = template.Library()


@register.simple_tag(name="lcs")
def get_const_string(value):
    """
    Template tag for accessing constants from LITE content library (not for Python use - only HTML)
    """

    def get(object_to_search, nested_properties_list):
        """
        Recursive function used to search an unknown number of nested objects
        for a property. For example if we had a path 'cases.CasePage.title' this function
        would take the current object `object_to_search` and get an object called 'CasePage'.
        It would then call itself again to search the 'CasePage' for a property called 'title'.
        :param object_to_search: An unknown object to get the given property from
        :param nested_properties_list: The path list to the attribute we want
        :return: The attribute in the given object for the given path
        """
        object = getattr(object_to_search, nested_properties_list[0])
        if len(nested_properties_list) == 1:
            # We have reached the end of the path and now have the string
            return object
        else:
            # Search the object for the next property in `nested_properties_list`
            return get(object, nested_properties_list[1:])

    warnings.warn("Reference constants from strings directly, only use LCS in HTML files", Warning)
    try:
        path = value.split(".")
        # Get initial object from strings.py
        path_object = getattr(strings, path[0])
        return get(path_object, path[1:])
    except AttributeError:
        return "STRING_NOT_FOUND"


@register.simple_tag
def get_string(value):
    """
    Given a string, such as 'cases.manage.attach_documents' it will return the relevant value
    from the strings.json file
    """
    warnings.warn(
        'get_string is deprecated. Use "lcs" instead, or reference constants from strings directly.', DeprecationWarning
    )

    # Pull the latest changes from strings.json for faster debugging
    if env("DEBUG"):
        with open("lite_content/lite-internal-frontend/strings.json") as json_file:
            lite_strings.constants = json.load(json_file)

    def get(d, keys):
        if "." in keys:
            key, rest = keys.split(".", 1)
            return get(d[key], rest)
        else:
            return d[keys]

    return get(lite_strings.constants, value)


@register.filter
@stringfilter
def str_date(value):
    return_value = do_timezone(datetime.datetime.strptime(value, ISO8601_FMT), "Europe/London")
    return (
        return_value.strftime("%-I:%M")
        + return_value.strftime("%p").lower()
        + " "
        + return_value.strftime("%d %B " "%Y")
    )


@register.filter()
def sentence_case(value):
    return stringcase.sentencecase(value)


@register.filter()
def reference_code(value):
    value = str(value)
    return value[:5] + "-" + value[5:]


@register.filter()
def add_selected_class(key, url):
    if key == url:
        return "lite-menu-item--selected"

    return ""


@register.filter()
def table_sort(key, actual_sort):
    actual_sort = actual_sort.get("sort")

    if not actual_sort:
        return ""

    if actual_sort == key:
        return "lite-cases-table__heading--active"

    if "-" + key in actual_sort:
        return "lite-cases-table__heading--active-desc"


@register.filter()
def table_sort_text(key, actual_sort):
    actual_sort = actual_sort.get("sort")

    if not actual_sort:
        return key

    if "-" + key in actual_sort:
        return ""

    if key in actual_sort:
        return "-" + key


@register.filter()
def add_subnav_selected_class(key, url):
    if key in url:
        return "lite-subnav__link--selected"

    return ""


@register.filter()
def group_list(items, split):
    """
    Groups items in a list based on a specified size
    """
    return [items[x : x + split] for x in range(0, len(items), split)]


@register.filter
@mark_safe
def pretty_json(value):
    """
    Pretty print JSON - for development purposes only.
    """
    return "<pre>" + json.dumps(value, indent=4) + "</pre>"


@register.filter(name="times")
def times(number):
    return [x + 1 for x in range(number)]


def replace_all(text, old, new):
    while old in text:
        text = text.replace(old, new)
    return text


@register.filter(name="old_character")
def old_character(text, old_char):
    return replace_all(text, old_char, "$$")


@register.filter(name="new_character")
def new_character(text, new_char):
    return replace_all(text, "$$", new_char)


@register.simple_tag
@mark_safe
def hidden_field(key, value):
    """
    Generates a hidden field from the given key and value
    """
    return f'<input type="hidden" name="{key}" value="{value}">'


@register.filter()
def friendly_boolean(boolean):
    """
    Returns 'Yes' if a boolean is equal to True, else 'No'
    """
    if boolean is True or boolean == "true" or boolean == "True":
        return "Yes"
    else:
        return "No"


@register.filter()
def get_first_country_from_first_good(dictionary: dict):
    """
    Returns the first key in a dictionary
    """
    return list(dictionary)[0] + "." + next(iter(dictionary.values()))[0]


@register.filter()
def get_end_user(application: dict):
    if application.get("end_user"):
        return application.get("end_user")
    return application.get("destinations").get("data")
