from conf.client import get, patch, post
from conf.constants import OPEN_GENERAL_LICENCES_URL
from core.helpers import convert_parameters_to_query_params


def get_open_general_licences(
    request, page=1, name=None, case_type=None, control_list_entry=None, country=None, status=None
):
    return get(request, OPEN_GENERAL_LICENCES_URL + convert_parameters_to_query_params(locals())).json()


def post_open_general_licences(request, json):
    response = post(request, OPEN_GENERAL_LICENCES_URL, json)
    return response.json(), response.status_code


def get_open_general_licence(request, pk):
    return get(request, OPEN_GENERAL_LICENCES_URL + str(pk)).json()


def patch_open_general_licence(request, pk, json):
    response = patch(request, OPEN_GENERAL_LICENCES_URL + str(pk), json)
    return response.json(), response.status_code


def set_open_general_licence_status(request, pk, json):
    if "status" not in json:
        return {"errors": {"response": ["Please pick one"]}}, 400

    response = patch(request, OPEN_GENERAL_LICENCES_URL + str(pk), json)
    return response.json(), response.status_code
