from django.http import HttpRequest

from core.builtins.custom_tags import get_string
from libraries.forms.components import Form, Filter, Checkboxes
from users.services import get_gov_users


def assign_users_form(request: HttpRequest, team_id, multiple: bool):
    return Form(get_string('cases.manage.assign_users.multiple_title') if multiple else get_string('cases.manage.assign_users.title'),
                get_string('cases.manage.assign_users.description'),
                [
                    Filter(),
                    Checkboxes('users', get_gov_users(request, {'teams': team_id},
                                                      convert_to_options=True))
                ],
                default_button_name='Submit',
                javascript_imports=['/assets/javascripts/filter-checkbox-list.js'])
