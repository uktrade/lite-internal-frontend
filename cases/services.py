from _decimal import Decimal

from cases.helpers import clean_advice
from conf.client import post, get, put, delete
from conf.constants import (
    CASE_URL,
    CASE_NOTES_URL,
    APPLICATIONS_URL,
    ACTIVITY_URL,
    DOCUMENTS_URL,
    END_USER_ADVISORY_URL,
    CASE_FLAGS_URL,
    ECJU_QUERIES_URL,
    GOOD_URL,
    FLAGS_URL,
    ASSIGN_FLAGS_URL,
    GOODS_TYPE_URL,
    USER_ADVICE_URL,
    TEAM_ADVICE_URL,
    FINAL_ADVICE_URL,
    VIEW_TEAM_ADVICE_URL,
    VIEW_FINAL_ADVICE_URL,
    GOOD_CLC_REVIEW_URL,
    MANAGE_STATUS_URL,
    FINAL_DECISION_URL,
    DURATION_URL,
    GENERATED_DOCUMENTS_URL,
    GENERATED_DOCUMENTS_PREVIEW_URL,
    DESTINATION_URL,
    CASE_OFFICER_URL,
    CASE_TYPES_URL,
    GOODS_QUERIES_URL,
    CLC_RESPONSE_URL,
    PV_GRADING_RESPONSE_URL,
    DECISIONS_URL,
    FINALISE_CASE_URL,
    QUEUES_URL,
)
from core.helpers import convert_parameters_to_query_params


# Case types
def get_case_types(request, type_only=True):
    data = get(request, CASE_TYPES_URL + "?type_only=" + str(type_only))
    return data.json()["case_types"]


# Case
def get_case(request, pk):
    data = get(request, CASE_URL + str(pk))
    return data.json()["case"]


# Case Queues
def put_case_queues(request, pk, json):
    data = put(request, CASE_URL + str(pk) + QUEUES_URL, json)
    return data.json(), data.status_code


# Queue assignment actions
def get_user_case_queues(request, pk):
    data = get(request, CASE_URL + str(pk) + "/assigned-queues/")
    return data.json()["queues"], data.status_code


def put_unassign_queues(request, pk, json):
    data = put(request, CASE_URL + str(pk) + "/assigned-queues/", json)
    return data.json(), data.status_code


# Applications
def put_application_status(request, pk, json):
    data = put(request, APPLICATIONS_URL + pk + MANAGE_STATUS_URL, json)
    return data.json(), data.status_code


def get_finalise_application_goods(request, pk):
    data = get(request, f"{APPLICATIONS_URL}{pk}{FINAL_DECISION_URL}")
    return data.json(), data.status_code


def finalise_application(request, pk, json):
    return put(request, f"{APPLICATIONS_URL}{pk}{FINAL_DECISION_URL}", json)


def get_application_default_duration(request, pk):
    return int(get(request, f"{APPLICATIONS_URL}{pk}{DURATION_URL}").json()["licence_duration"])


# Goods Queries
def put_goods_query_clc(request, pk, json):
    # This is a workaround due to RespondCLCQuery not using a SingleFormView
    if "control_list_entries[]" in json:
        json["control_list_entries"] = json.getlist("control_list_entries[]")

    data = put(request, GOODS_QUERIES_URL + pk + CLC_RESPONSE_URL, json)
    return data.json(), data.status_code


def put_goods_query_pv_grading(request, pk, json):
    data = put(request, GOODS_QUERIES_URL + pk + PV_GRADING_RESPONSE_URL, json)
    return data.json(), data.status_code


def put_goods_query_status(request, pk, json):
    data = put(request, GOODS_QUERIES_URL + pk + MANAGE_STATUS_URL, json)
    return data.json(), data.status_code


# EUA Queries
def put_end_user_advisory_query(request, pk, json):
    data = put(request, END_USER_ADVISORY_URL + str(pk), json)
    return data.json(), data.status_code


# Case Notes
def get_case_notes(request, pk):
    data = get(request, CASE_URL + pk + CASE_NOTES_URL)
    return data.json(), data.status_code


def post_case_notes(request, pk, json):
    data = post(request, CASE_URL + pk + CASE_NOTES_URL, json)
    return data.json(), data.status_code


# Case Flags
def put_case_flags(request, pk, flags):
    data = put(request, CASE_URL + pk + CASE_FLAGS_URL, flags)
    return data.json(), data.status_code


# Activity
def get_activity(request, pk):
    data = get(request, CASE_URL + pk + ACTIVITY_URL + "?fields=status,flags")
    return data.json()["activity"]


# Case Documents
def get_case_document(request, pk, document_metadata_id):
    data = get(request, CASE_URL + pk + DOCUMENTS_URL + document_metadata_id)
    return data.json(), data.status_code


def get_case_documents(request, pk):
    data = get(request, CASE_URL + pk + DOCUMENTS_URL)
    return data.json(), data.status_code


def post_case_documents(request, pk, json):
    data = post(request, CASE_URL + pk + DOCUMENTS_URL, json)
    return data.json(), data.status_code


def delete_case_document(request, pk, s3_key):
    data = delete(request, CASE_URL + pk + DOCUMENTS_URL + s3_key)
    return data.json(), data.status_code


# Advice
def get_user_case_advice(request, case_pk):
    data = get(request, CASE_URL + case_pk + USER_ADVICE_URL)
    return data.json(), data.status_code


def get_team_case_advice(request, case_pk, team_pk):
    data = get(request, CASE_URL + case_pk + VIEW_TEAM_ADVICE_URL + team_pk)
    return data.json(), data.status_code


def coalesce_user_advice(request, case_pk):
    data = get(request, CASE_URL + case_pk + TEAM_ADVICE_URL)
    return data.json(), data.status_code


def clear_team_advice(request, case_pk):
    data = delete(request, CASE_URL + case_pk + TEAM_ADVICE_URL)
    return data.json(), data.status_code


def get_final_case_advice(request, case_pk):
    data = get(request, CASE_URL + case_pk + VIEW_FINAL_ADVICE_URL)
    return data.json(), data.status_code


def get_final_decision_documents(request, case_pk):
    data = get(request, CASE_URL + case_pk + "/final-advice-documents/")
    return data.json(), data.status_code


def grant_licence(request, case_pk):
    data = put(request, CASE_URL + case_pk + FINALISE_CASE_URL, {})
    return data.json(), data.status_code


def get_licence(request, case_pk):
    data = get(request, CASE_URL + case_pk + FINALISE_CASE_URL)
    return data.json(), data.status_code


def coalesce_team_advice(request, case_pk):
    data = get(request, CASE_URL + case_pk + FINAL_ADVICE_URL)
    return data.json(), data.status_code


def clear_final_advice(request, case_pk):
    data = delete(request, CASE_URL + case_pk + FINAL_ADVICE_URL)
    return data.json(), data.status_code


def return_non_empty(data):
    for item in data:
        if item:
            return item


def build_case_advice(key, value, base_data):
    data = base_data.copy()
    data[key] = value
    return data


def prepare_data_for_advice(json):
    json = clean_advice(json)

    # Split the json data into multiple
    base_data = {"type": json["type"], "text": json["advice"], "note": json["note"]}

    if json.get("type") == "refuse":
        base_data["denial_reasons"] = json["denial_reasons"]

    if json.get("type") == "proviso":
        base_data["proviso"] = json["proviso"]

    if json.get("pv_grading"):
        base_data["pv_grading"] = json["pv_grading"]

    new_data = []
    single_cases = ["end_user", "consignee"]
    multiple_cases = {
        "ultimate_end_users": "ultimate_end_user",
        "third_parties": "third_party",
        "countries": "country",
        "goods": "good",
        "goods_types": "goods_type",
    }

    for entity_name in single_cases:
        if json.get(entity_name):
            new_data.append(build_case_advice(entity_name, json.get(entity_name), base_data))

    for entity_name, entity_name_singular in multiple_cases.items():
        if json.get(entity_name):
            for entity in json.get(entity_name, []):
                new_data.append(build_case_advice(entity_name_singular, entity, base_data))

    return new_data


def get_good_countries_decisions(request, case_pk):
    data = get(request, CASE_URL + case_pk + "/goods-countries-decisions/")
    return data.json()


def post_good_countries_decisions(request, case_pk, json):
    data = post(request, CASE_URL + case_pk + "/goods-countries-decisions/", json)
    return data.json(), data.status_code


def post_user_case_advice(request, case_pk, json):
    new_data = prepare_data_for_advice(json)
    data = post(request, CASE_URL + case_pk + USER_ADVICE_URL, new_data)
    return data.json(), data.status_code


def post_team_case_advice(request, case_pk, json):
    new_data = prepare_data_for_advice(json)
    data = post(request, CASE_URL + case_pk + TEAM_ADVICE_URL, new_data)
    return data.json(), data.status_code


def post_final_case_advice(request, case_pk, json):
    new_data = prepare_data_for_advice(json)
    data = post(request, CASE_URL + case_pk + FINAL_ADVICE_URL, new_data)
    return data.json(), data.status_code


def get_document(request, pk):
    data = get(request, DOCUMENTS_URL + pk)
    return data.json(), data.status_code


# ECJU Queries
def get_ecju_queries(request, pk):
    data = get(request, CASE_URL + pk + ECJU_QUERIES_URL)
    return data.json(), data.status_code


def post_ecju_query(request, pk, json):
    data = post(request, CASE_URL + pk + ECJU_QUERIES_URL, json)
    return data.json(), data.status_code


def get_good(request, pk):
    data = get(request, GOOD_URL + pk)
    return data.json(), data.status_code


def get_goods_type(request, pk):
    data = get(request, GOODS_TYPE_URL + pk)
    return {"good": data.json()}, data.status_code


def post_goods_control_code(request, case_id, json):
    # Data will only be passed back when a error is thrown with status code of 400, as such it is not split here.
    response = post(request, GOOD_CLC_REVIEW_URL + case_id + "/", json)
    return response


# Good Flags
def get_flags_for_team_of_level(request, level, team_id, include_system_flags=False):
    """
    :param request: headers for the request
    :param level: 'cases', 'goods'
    :param include_system_flags: used to indicate adding system flags to list of team flags returned
    :return:
    """
    data = get(request, FLAGS_URL + convert_parameters_to_query_params(locals()) + "&disable_pagination=True")
    return data.json(), data.status_code


def put_flag_assignments(request, json):
    data = put(request, ASSIGN_FLAGS_URL, json)
    return data.json(), data.status_code


def _generate_data_and_keys(request, pk):
    case = get_case(request, pk)
    case_advice, _ = get_final_case_advice(request, pk)

    # The keys are each relevant good-country pairing in the format good_id.country_id
    keys = []
    # Builds form page data structure
    # For each good in the case
    for good in case["application"]["goods_types"]:
        # Match the goods with the goods in advice for that case
        # and attach the advice value to the good
        for advice in case_advice["advice"]:
            if advice["goods_type"] == good["id"]:
                good["advice"] = advice["type"]
                break
        # If the good has countries attached to it as destinations
        # We do the same with the countries and their advice
        if good["countries"]:
            for country in good["countries"]:
                keys.append(str(good["id"]) + "." + country["id"])
                for advice in case_advice["advice"]:
                    if advice["country"] == country["id"]:
                        country["advice"] = advice["type"]
                        break
        # If the good has no countries:
        else:
            good["countries"] = []
            # We attach all countries from the case
            # And then attach the advice as before
            for country in case["application"]["destinations"]["data"]:
                good["countries"].append(country)
                keys.append(str(good["id"]) + "." + country["id"])
                for advice in case_advice["advice"]:
                    if advice["country"] == country["id"]:
                        country["advice"] = advice["type"]
                        break
    data = get_good_countries_decisions(request, pk)
    if "detail" in data:
        raise PermissionError

    return case, data, keys


def _generate_post_data_and_errors(keys, request_data, action):
    post_data = []
    errors = {}
    for key in keys:
        good_pk = key.split(".")[0]
        country_pk = key.split(".")[1]
        if key not in request_data and not action == "save":
            if good_pk in errors:
                errors[good_pk].append(country_pk)
            else:
                errors[good_pk] = [country_pk]
        else:
            post_data.append({"good": good_pk, "country": country_pk, "decision": request_data.get(key)})
    return post_data, errors


def _get_total_goods_value(case):
    total_value = 0
    for good in case.get("application").get("goods", []):
        # conditional, as some case types e.g. exhibition clearances don't contain a value.
        if good.get("value"):
            total_value += Decimal(good["value"]).quantize(Decimal(".01"))
    return total_value


# Letter template decisions
def get_decisions(request):
    data = get(request, DECISIONS_URL)
    return data.json()["decisions"], data.status_code


# Generated Documents
def post_generated_document(request, pk, json):
    data = post(request, CASE_URL + pk + GENERATED_DOCUMENTS_URL, json)
    return data.status_code


def get_generated_document_preview(request, pk, tpk, text):
    data = get(request, CASE_URL + pk + GENERATED_DOCUMENTS_PREVIEW_URL + "?template=" + tpk + "&text=" + text)
    return data.json(), data.status_code


def get_generated_document(request, pk, dpk):
    data = get(request, CASE_URL + str(pk) + GENERATED_DOCUMENTS_URL + str(dpk) + "/")
    return data.json(), data.status_code


def get_destination(request, pk):
    data = get(request, DESTINATION_URL + pk)
    return data.json()


def get_case_officer(request, pk):
    data = get(request, CASE_URL + pk + CASE_OFFICER_URL)
    return data.json()["case_officer"], data.status_code


def put_case_officer(request, pk, user_pk):
    data = put(request, CASE_URL + pk + CASE_OFFICER_URL, json={"gov_user_pk": user_pk})
    return data, data.status_code


def delete_case_officer(request, pk):
    data = delete(request, CASE_URL + pk + CASE_OFFICER_URL)
    return data, data.status_code


def get_case_additional_contacts(request, pk):
    response = get(request, CASE_URL + str(pk) + "/additional-contacts/")
    return response.json()


def post_case_additional_contacts(request, pk, json):
    response = post(request, CASE_URL + str(pk) + "/additional-contacts/", json=json)
    return response.json(), response.status_code
