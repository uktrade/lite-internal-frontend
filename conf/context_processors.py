import os

from django.urls import reverse_lazy

from conf.constants import Permissions
from core.helpers import has_permission
from lite_content.lite_internal_frontend import strings
from lite_forms.helpers import conditional


def export_vars(request):
    return {"ENVIRONMENT_VARIABLES": dict(os.environ.items())}


def lite_menu(request):
    pages = [
        {"title": "Cases", "url": reverse_lazy("cases:cases"), "icon": "menu/cases"},
        {"title": "Organisations", "url": reverse_lazy("organisations:organisations"), "icon": "menu/businesses"},
        {"title": "Teams", "url": reverse_lazy("teams:teams"), "icon": "menu/teams"},
        {"title": "My Team", "url": reverse_lazy("teams:team"), "icon": "menu/teams"},
        {"title": "Queues", "url": reverse_lazy("queues:queues"), "icon": "menu/queues"},
        {"title": "Users", "url": reverse_lazy("users:users"), "icon": "menu/users"},
        {"title": "Flags", "url": reverse_lazy("flags:flags"), "icon": "menu/flags"},
        conditional(
            has_permission(request, Permissions.CONFIGURE_TEMPLATES),
            {
                "title": strings.DOCUMENT_TEMPLATES_TITLE,
                "url": reverse_lazy("letter_templates:letter_templates"),
                "icon": "menu/letter_templates",
            },
        ),
        {"title": "HMRC", "url": reverse_lazy("organisations:hmrc"), "icon": "menu/businesses"},
    ]

    return {"LITE_MENU": [x for x in pages if x is not None]}
