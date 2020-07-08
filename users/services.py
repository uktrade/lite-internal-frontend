from http import HTTPStatus
from urllib.parse import urlencode

from conf.client import get, post, put
from conf.constants import (
    GOV_USERS_URL,
    GOV_USERS_ROLES_URL,
    GOV_USERS_PERMISSIONS_URL,
    SUPER_USER_ROLE_ID,
)
from lite_content.lite_internal_frontend.users import AssignUserPage
from lite_forms.components import Option


def get_gov_users(request, params=None, convert_to_options=False):
    if params:
        query_params = urlencode(params)
        data = get(request, GOV_USERS_URL + "?" + query_params)
    else:
        data = get(request, GOV_USERS_URL)

    if convert_to_options:
        converted = []

        for user in data.json()["results"]:
            first_name = user.get("first_name")
            last_name = user.get("last_name")
            email = user.get("email")

            if first_name:
                value = first_name + " " + last_name
                description = email
            else:
                value = email
                description = None

            # Hide users without emails (eg system users)
            if email:
                converted.append(Option(key=user.get("id"), value=value, description=description))

        return converted
    return data.json(), data.status_code


def get_gov_user(request, pk=None):
    if pk:
        data = get(request, GOV_USERS_URL + str(pk))
    else:
        data = get(request, GOV_USERS_URL + "me/")
    return data.json(), data.status_code


def get_gov_user_from_form_selection(request, pk, json):
    user = json.get("user")
    if user:
        data = get(request, GOV_USERS_URL + json.get("user"))
        return data.json(), data.status_code
    return {"errors": {"user": [AssignUserPage.USER_ERROR_MESSAGE]}}, HTTPStatus.BAD_REQUEST


def post_gov_users(request, json):
    data = post(request, GOV_USERS_URL, json)
    return data.json(), data.status_code


def put_gov_user(request, pk, json):
    data = put(request, GOV_USERS_URL + str(pk) + "/", json)
    return data.json(), data.status_code


# Roles and Permissions
def get_roles(request, convert_to_options=False):
    data = get(request, GOV_USERS_ROLES_URL)

    if convert_to_options:
        converted = []

        for item in data.json().get("roles"):
            converted.append(Option(key=item["id"], value=item["name"]))

        return converted

    return data.json(), data.status_code


def get_role(request, pk):
    data = get(request, GOV_USERS_ROLES_URL + pk)
    return data.json(), data.status_code


def post_role(request, json):
    data = post(request, GOV_USERS_ROLES_URL, json)
    return data.json(), data.status_code


def put_role(request, pk, json):
    data = put(request, GOV_USERS_ROLES_URL + pk + "/", json)
    return data.json(), data.status_code


def get_permissions(request, convert_to_options=False):
    data = get(request, GOV_USERS_PERMISSIONS_URL)

    if convert_to_options:
        converted = []

        for item in data.json().get("permissions"):
            converted.append(Option(key=item["id"], value=item["name"]))

        return converted

    return data.json()["permissions"]


def is_super_user(user):
    return user["user"]["role"]["id"] == SUPER_USER_ROLE_ID
