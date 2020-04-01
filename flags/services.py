import functools

from core.helpers import convert_dict_to_query_params, convert_parameters_to_query_params
from lite_forms.components import Option

from conf.client import get, post, put, patch
from conf.constants import FLAGS_URL, FLAGGING_RULES


def get_flags(request, page=1, only_show_deactivated=False, team_pk=None):
    data = get(request, FLAGS_URL + convert_parameters_to_query_params(locals()))
    return data.json()


def _get_team_flags(level, request, convert_to_options=False, include_deactivated=False):
    data = get(
        request,
        f"{FLAGS_URL}?level={level}&team=True&include_deactivated={include_deactivated}?disable_pagination=True",
    ).json()["results"]

    if convert_to_options:
        return [Option(key=flag["id"], value=flag["name"]) for flag in data]

    return data


get_cases_flags = functools.partial(_get_team_flags, "Case")
get_goods_flags = functools.partial(_get_team_flags, "Good")
get_organisation_flags = functools.partial(_get_team_flags, "Organisation")
get_destination_flags = functools.partial(_get_team_flags, "Destination")


def post_flags(request, json):
    data = post(request, FLAGS_URL, json)
    return data.json(), data.status_code


def get_flag(request, pk):
    data = get(request, FLAGS_URL + pk)
    return data.json()


def update_flag(request, pk, json):
    data = patch(request, FLAGS_URL + pk + "/", json)
    return data.json(), data.status_code


def get_flagging_rules(request, params):
    data = get(request, FLAGGING_RULES + "?" + params)
    return data.json(), data.status_code


def post_flagging_rules(request, json):
    data = post(request, FLAGGING_RULES, json)
    return data.json(), data.status_code


def get_flagging_rule(request, pk):
    data = get(request, FLAGGING_RULES + str(pk))
    return data.json(), data.status_code


def put_flagging_rule(request, pk, json):
    data = json
    if json.get("form_name"):
        data["status"] = json.get("form_name")
    data = put(request, FLAGGING_RULES + str(pk), json)
    return data.json(), data.status_code
