from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from cases.constants import CaseType
from lite_forms.generators import error_page, form_page

from cases.forms.advice import advice_recommendation_form
from cases.helpers import check_matching_advice, add_hidden_advice_data, clean_advice
from cases.services import get_case, _get_total_goods_value
from core.services import get_denial_reasons, get_user_permissions, get_status_properties, get_pv_gradings
from picklists.services import get_picklists_for_input
from teams.services import get_teams
from users.services import get_gov_user
from conf.constants import Permission, APPLICATION_CASE_TYPES, CLEARANCE_CASE_TYPES, CONFLICTING


def get_case_advice(get_advice, request, case, advice_level, team=None):
    """
    :param get_advice: This is a service method to get the advice from a particular level
    :param case: Case DTO returned form API in the dispatch
    :param advice_level: This is a choice of "user", "team" or "final"
    :param team: Optional team object, only used if getting the advice for a case at the team level
    :return: A page with all the advice for a case at the user level, team level for a chosen team or a final level
    """
    if team:
        advice, _ = get_advice(request, case.get("id"), team.get("id"))
    else:
        advice, _ = get_advice(request, case.get("id"))

    permissions, user_team = get_user_permissions(request, True)

    context = {
        "case": case,
        "all_advice": advice["advice"],
        "total_goods_value": _get_total_goods_value(case),
        "permitted_to_give_final_advice": _check_user_permitted_to_give_final_advice(
            case["application"]["case_type"]["sub_type"]["key"], permissions
        ),
        "can_create_and_edit_advice": _can_user_create_and_edit_advice(case, permissions),
        "can_advice_be_finalised": _can_advice_be_finalised(advice),
        "can_manage_team_advice": Permission.MANAGE_TEAM_ADVICE.value in permissions,
    }

    if team:
        context["team"] = team
        context["is_user_team"] = team.get("id") == user_team.get("id")
        teams, _ = get_teams(request)
        context["teams"] = teams["teams"]

    if "application" in case:
        status_props, _ = get_status_properties(request, case["application"]["status"]["key"])
    else:
        status_props, _ = get_status_properties(request, case["query"]["status"]["key"])

    context["status_is_read_only"] = status_props["is_read_only"]
    context["status_is_terminal"] = status_props["is_terminal"]

    return render(request, f"case/advice/{advice_level}.html", context)


def _check_user_permitted_to_give_final_advice(case_type, permissions):
    """ Check if the user is permitted to give final advice on the case based on their
    permissions and the case type. """
    if case_type in APPLICATION_CASE_TYPES and Permission.MANAGE_LICENCE_FINAL_ADVICE.value in permissions:
        return True
    elif case_type in CLEARANCE_CASE_TYPES and Permission.MANAGE_CLEARANCE_FINAL_ADVICE.value in permissions:
        return True
    else:
        return False


def _can_advice_be_finalised(advice):
    """Check that there is no conflicting advice and that the advice can be finalised. """
    for item in advice["advice"]:
        if item["type"]["key"] == CONFLICTING:
            return False
    return True


def _can_user_create_and_edit_advice(case, permissions):
    """Check that the user can create and edit advice. """
    return Permission.MANAGE_TEAM_CONFIRM_OWN_ADVICE.value in permissions or (
        Permission.MANAGE_TEAM_ADVICE.value in permissions and not case.get("has_advice").get("my_user")
    )


def render_form_page(get_advice, request, case, form, team=None):
    """
    :param get_advice: This is a service method to get the advice from a particular level
    :param case: Case DTO returned form API in the dispatch
    :param form: To be rendered
    :param team: Optional team object, only used if getting the advice for a case at the team level
    :return: Form page for selecting advice type with pre-populating data if it matches
    """
    if team:
        advice, _ = get_advice(request, case.get("id"), team.get("id"))
    else:
        advice, _ = get_advice(request, case.get("id"))

    selected_advice_data = request.POST
    pre_data = check_matching_advice(request.user.lite_api_user_id, advice["advice"], selected_advice_data)

    # Validate at least one checkbox is checked
    if not len(selected_advice_data) > 0:
        return error_page(request, "Select at least one good or destination to give advice on")

    # Add data to the form as hidden fields
    form.questions = add_hidden_advice_data(form.questions, selected_advice_data)

    return form_page(request, form, data=pre_data)


def post_advice(get_advice, request, case, form, user_team_final, team=None):
    """
    :param get_advice: This is a service method to get the advice from a particular level
    :param case: Case DTO returned form API in the dispatch
    :param form: To be rendered
    :param user_team_final: This is a choice of "user", "team" or "final"
    :param team: Optional team object, only used if getting the advice for a case at the team level
    :return:
    """
    selected_advice_data = request.POST
    if team:
        advice, _ = get_advice(request, case.get("id"), team.get("id"))
    else:
        advice, _ = get_advice(request, case.get("id"))
    pre_data = check_matching_advice(request.user.lite_api_user_id, advice["advice"], selected_advice_data)

    if pre_data and not str(selected_advice_data["type"]) in str(pre_data["type"]):
        pre_data = None

    # Validate at least one radiobutton is selected
    if not selected_advice_data.get("type"):
        # Add data to the error form as hidden fields
        form.questions = add_hidden_advice_data(form.questions, selected_advice_data)

        return form_page(request, form, errors={"type": ["Select a decision"]})

    # Render the advice detail page
    proviso_picklist_items = get_picklists_for_input(request, "proviso")
    advice_picklist_items = get_picklists_for_input(request, "standard_advice")
    static_denial_reasons, _ = get_denial_reasons(request, False)

    form = "case/give-advice.html"

    context = {
        "case": case,
        "title": "Give advice",
        "type": selected_advice_data.get("type"),
        "proviso_picklist": proviso_picklist_items["picklist_items"],
        "advice_picklist": advice_picklist_items["picklist_items"],
        "static_denial_reasons": static_denial_reasons,
        "pv_gradings": get_pv_gradings(request),
        # Add previous data
        "goods": selected_advice_data.get("goods"),
        "goods_types": selected_advice_data.get("goods_types"),
        "countries": selected_advice_data.get("countries"),
        "end_user": selected_advice_data.get("end_user"),
        "ultimate_end_users": selected_advice_data.get("ultimate_end_users"),
        "third_parties": selected_advice_data.get("third_parties"),
        "consignee": selected_advice_data.get("consignee"),
        "data": pre_data,
        "level": user_team_final,
        "show_clearance": CaseType.is_mod(case["case_type"]["sub_type"]["key"]),
    }
    return render(request, form, context)


def post_advice_details(post_case_advice, request, case, form, user_team_final, **kwargs):
    """
    :param post_case_advice: This is a service method to post the advice for a particular level
    :param case: The case DTO returned by the API
    :param form: To be rendered
    :param user_team_final: This is a choice of "user", "team" or "final"
    :return:
    """
    data = request.POST
    response, _ = post_case_advice(request, case.get("id"), data)

    if "errors" in response:
        proviso_picklist_items = get_picklists_for_input(request, "proviso")
        advice_picklist_items = get_picklists_for_input(request, "standard_advice")
        static_denial_reasons, _ = get_denial_reasons(request, False)

        data = clean_advice(data)

        context = {
            "case": case,
            "title": "Error: Give advice",
            "type": data.get("type"),
            "proviso_picklist": proviso_picklist_items["picklist_items"],
            "advice_picklist": advice_picklist_items["picklist_items"],
            "static_denial_reasons": static_denial_reasons,
            "pv_gradings": get_pv_gradings(request),
            # Add previous data
            "goods": data.get("goods"),
            "goods_types": data.get("goods_types"),
            "countries": data.get("countries"),
            "end_user": data.get("end_user"),
            "ultimate_end_users": data.get("ultimate_end_users"),
            "third_parties": data.get("third_parties"),
            "consignee": data.get("consignee"),
            "errors": response["errors"][0],
            "data": data,
            "level": user_team_final,
        }
        return render(request, form, context)

    # Add success message
    messages.success(request, "Your advice has been posted successfully")

    return redirect(
        reverse_lazy(
            "cases:" + user_team_final + "_advice_view", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case.get("id")}
        )
    )


def give_advice_dispatch(user_team_final, request, **kwargs):
    """
    Returns the case and the form for the level of the advice to be used in the end points
    """
    case = get_case(request, str(kwargs["pk"]))
    post_endpoint = reverse_lazy(
        "cases:give_" + user_team_final + "_advice", kwargs={"queue_pk": kwargs["queue_pk"], "pk": str(kwargs["pk"])}
    )
    back_endpoint = reverse_lazy(
        "cases:" + user_team_final + "_advice_view", kwargs={"queue_pk": kwargs["queue_pk"], "pk": str(kwargs["pk"])}
    )
    form = advice_recommendation_form(post_endpoint, back_endpoint, case["application"]["case_type"]["sub_type"]["key"])

    if user_team_final == "team":
        user, _ = get_gov_user(request)
        team = user["user"]["team"]
        return case, form, team

    return case, form


def give_advice_detail_dispatch(request, **kwargs):
    """
    Returns the case to be used in the end point and validates advice type selection
    """
    case = get_case(request, str(kwargs["pk"]))

    # If the advice type is not valid, raise a 404
    advice_type = kwargs["type"]
    if advice_type not in ["approve", "proviso", "refuse", "no_licence_required", "not_applicable"]:
        raise Http404

    return case
