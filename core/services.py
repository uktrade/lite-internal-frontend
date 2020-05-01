from cases.constants import CaseType
from lite_forms.components import Option, Checkboxes

from conf.client import get
from conf.constants import (
    DENIAL_REASONS_URL,
    COUNTRIES_URL,
    STATUSES_URL,
    CONTROL_LIST_ENTRIES_URL,
    NOTIFICATIONS_URL,
    STATUS_PROPERTIES_URL,
    GOV_PV_GRADINGS_URL,
    Statuses,
    GOODS_QUERY_STATUSES,
    PV_GRADINGS_URL,
)
from users.services import get_gov_user


def get_denial_reasons(request, convert_to_options=False):
    data = get(request, DENIAL_REASONS_URL).json()["denial_reasons"]

    if convert_to_options:
        return [Option(denial_reason["id"], denial_reason["id"]) for denial_reason in data]
    else:
        return data


def get_countries(request, convert_to_options=False, exclude: list = None):
    """
    Returns a list of GOV.UK countries and territories
    param exclude: Takes a list of country codes and excludes them
    """
    from core.helpers import convert_value_to_query_param

    data = get(request, COUNTRIES_URL + "?" + convert_value_to_query_param("exclude", exclude))

    if convert_to_options:
        converted_units = []

        for country in data.json().get("countries"):
            converted_units.append(Option(country.get("id"), country.get("name")))

        return converted_units

    return data.json(), data.status_code


# Statuses
def get_statuses(request, convert_to_options=False):
    """ Get static list of case statuses. """
    data = get(request, STATUSES_URL)

    if convert_to_options:
        return [Option(key=item["id"], value=item["value"]) for item in data.json().get("statuses")]

    return data.json()["statuses"], data.status_code


def get_permissible_statuses(request, case_type):
    """ Get a list of case statuses permissible for the user's role. """
    user, _ = get_gov_user(request, str(request.user.lite_api_user_id))
    user_permissible_statuses = user["user"]["role"]["statuses"]
    statuses, _ = get_statuses(request)

    if case_type == CaseType.APPLICATION.value:
        case_type_applicable_statuses = [
            status
            for status in statuses
            if status["key"]
            not in [Statuses.APPLICANT_EDITING, Statuses.CLOSED, Statuses.FINALISED, Statuses.REGISTERED]
        ]
    else:
        case_type_applicable_statuses = [status for status in statuses if status["key"] in GOODS_QUERY_STATUSES]

    return [status for status in case_type_applicable_statuses if status in user_permissible_statuses]


def get_status_properties(request, status):
    data = get(request, STATUS_PROPERTIES_URL + status)
    return data.json(), data.status_code


# Permissions
def get_user_permissions(request, with_team=False):
    user, _ = get_gov_user(request)
    if with_team:
        return user["user"]["role"]["permissions"], user["user"]["team"]
    return user["user"]["role"]["permissions"]


# Notifications
def get_notifications(request):
    data = get(request, NOTIFICATIONS_URL)
    return data.json()["notifications"]


# Control List Entries
def get_control_list_entries(request, convert_to_options=False):
    if convert_to_options:
        data = get(request, CONTROL_LIST_ENTRIES_URL + "?flatten=True")

        converted_units = []

        for control_list_entry in data.json()["control_list_entries"]:
            converted_units.append(
                Option(
                    key=control_list_entry["rating"],
                    value=control_list_entry["rating"],
                    description=control_list_entry["text"],
                )
            )

        return converted_units

    data = get(request, CONTROL_LIST_ENTRIES_URL)
    return data.json()["control_list_entries"]


def get_gov_pv_gradings(request, convert_to_options=False):
    pv_gradings = get(request, GOV_PV_GRADINGS_URL).json().get("pv_gradings")
    if convert_to_options:
        converted_units = []
        for pv_grading_entry in pv_gradings:
            for key in pv_grading_entry:
                converted_units.append(Option(key=key, value=pv_grading_entry[key]))
        return converted_units

    return pv_gradings


def get_pv_gradings(request):
    pv_gradings = get(request, PV_GRADINGS_URL).json().get("pv_gradings")
    return pv_gradings
