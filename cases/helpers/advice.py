from typing import List, Dict

from cases.objects import Case
from cases.services import get_blocking_flags
from conf.constants import APPLICATION_CASE_TYPES, Permission, CLEARANCE_CASE_TYPES
from core.builtins.custom_tags import filter_advice_by_level
from core.services import get_status_properties
from teams.services import get_teams


def get_destinations(request, case: Case):
    selected_destinations_ids = [*request.GET.getlist("ultimate_end_user"), *request.GET.getlist("countries"),
                                 *request.GET.getlist("third_party"), request.GET.get("end_user"),
                                 request.GET.get("consignee")]
    destinations = case.destinations
    return_values = []

    for destination in destinations:
        if destination["id"] in selected_destinations_ids:
            return_values.append(destination)

    return return_values


def get_goods(request, case: Case):
    selected_goods_ids = request.GET.getlist("goods", request.GET.getlist("goods_types"))
    goods = case.data.get("goods", case.data.get("goods_types"))
    return_values = []

    for good in goods:
        if "good" in good:
            if good["good"]["id"] in selected_goods_ids:
                return_values.append(good)
        else:
            if good["id"] in selected_goods_ids:
                return_values.append(good)

    return return_values


def get_advice_additional_context(request, case, permissions):
    status_props, _ = get_status_properties(request, case.data["status"]["key"])
    current_advice_level = "Advice"
    if filter_advice_by_level(case["advice"], "TeamAdvice"):
        current_advice_level = "TeamAdvice"
    if filter_advice_by_level(case["advice"], "FinalAdvice"):
        current_advice_level = "FinalAdvice"

    return {
        "permitted_to_give_final_advice": _check_user_permitted_to_give_final_advice(
            case["application"]["case_type"]["sub_type"]["key"], permissions
        ),
        "can_create_and_edit_advice": _can_user_create_and_edit_advice(case, permissions),
        "can_advice_be_finalised": _can_advice_be_finalised(case["advice"]),
        "can_manage_team_advice": Permission.MANAGE_TEAM_ADVICE.value in permissions,
        "is_user_team": True,
        "teams": get_teams(request),
        "status_is_read_only": status_props["is_read_only"],
        "status_is_terminal": status_props["is_terminal"],
        "current_advice_level": current_advice_level,
        "blocking_flags": get_blocking_flags(request, case["id"]),
    }


def flatten_advice_data(request, items: List[Dict]):
    if not items or not items[0].get("advice"):
        return

    first_item_advice = items[0]["advice"][0]
    keys = ["proviso", "denial_reasons", "note", "text", "type"]

    for item in items:
        for advice in [
            advice for advice in item.get("advice", []) if advice["user"]["id"] == request.user.lite_api_user_id
        ]:
            for key in keys:
                if advice[key] != first_item_advice[key]:
                    return

    return first_item_advice


def _check_user_permitted_to_give_final_advice(case_type, permissions):
    """ Check if the user is permitted to give final advice on the case based on their
    permissions and the case type. """
    if case_type in APPLICATION_CASE_TYPES and Permission.MANAGE_LICENCE_FINAL_ADVICE.value in permissions:
        return True
    elif case_type in CLEARANCE_CASE_TYPES and Permission.MANAGE_CLEARANCE_FINAL_ADVICE.value in permissions:
        return True
    else:
        return False


def _can_advice_be_finalised(case):
    """Check that there is no conflicting advice and that the advice can be finalised. """
    # items = [*case.goods, *case.destinations]
    #
    # for item in items:
    #     for advice in item.get("advice", []):
    #         if advice["type"]["key"] == AdviceType.CONFLICTING:
    #             return False
    return True


def _can_user_create_and_edit_advice(case, permissions):
    """Check that the user can create and edit advice. """
    return Permission.MANAGE_TEAM_CONFIRM_OWN_ADVICE.value in permissions or (
        Permission.MANAGE_TEAM_ADVICE.value in permissions and not case.get("has_advice").get("my_user")
    )
