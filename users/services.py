from urllib.parse import urlencode

from conf.client import get, post, put
from conf.constants import GOV_USERS_URL
from libraries.forms.components import Option


def get_gov_users(request, params=None, convert_to_options=False):
    if params:
        query_params = urlencode(params)
        data = get(request, GOV_USERS_URL + '?' + query_params)
    else:
        data = get(request, GOV_USERS_URL)

    if convert_to_options:
        converted = []

        for user in data.json().get('gov_users'):
            converted.append(
                Option(user.get('id'), user.get('first_name') + ' ' + user.get('last_name'))
            )

        return converted

    return data.json(), data.status_code


def get_gov_user(request, pk):
    data = get(request, GOV_USERS_URL + pk)
    return data.json(), data.status_code


def post_gov_users(request, json):
    data = post(request, GOV_USERS_URL, json)
    return data.json(), data.status_code


def put_gov_user(request, pk, json):
    data = put(request, GOV_USERS_URL + pk + "/", json)
    return data.json(), data.status_code
