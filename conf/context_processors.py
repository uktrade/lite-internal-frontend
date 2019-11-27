import os

from conf.constants import Permissions
from core.helpers import has_permission
from lite_forms.helpers import conditional


def export_vars(request):
    return {"ENVIRONMENT_VARIABLES": dict(os.environ.items())}


def lite_menu(request):
    pages = [
        {"title": "Cases", "url": "/cases/", "icon": "menu/cases"},
        {"title": "Organisations", "url": "/organisations/", "icon": "menu/businesses"},
        {"title": "Teams", "url": "/teams/", "icon": "menu/teams"},
        {"title": "My Team", "url": "/team", "icon": "menu/teams"},
        {"title": "Queues", "url": "/queues/", "icon": "menu/queues"},
        {"title": "Users", "url": "/users/", "icon": "menu/users"},
        {"title": "Flags", "url": "/flags/", "icon": "menu/flags"},
        conditional(
            has_permission(request, Permissions.CONFIGURE_TEMPLATES),
            {"title": "Letter Templates", "url": "/letter-templates/", "icon": "menu/letter_templates"},
        ),
        {"title": "HMRC", "url": "/organisations/hmrc/", "icon": "menu/businesses"},
    ]

    return {"LITE_MENU": [x for x in pages if x is not None]}
