from conf.client import post, get, put, delete
from conf.constants import CASE_URL, CASE_NOTES_URL, APPLICATIONS_URL, ACTIVITY_URL, CLC_QUERIES_URL, DOCUMENTS_URL, \
    CASE_FLAGS_URL, ADVICE_URL


def get_case(request, pk):
    data = get(request, CASE_URL + pk)
    return data.json(), data.status_code


def put_case(request, pk, json):
    data = put(request, CASE_URL + pk, json)
    return data.json(), data.status_code


# Applications
def put_applications(request, pk, json):
    data = put(request, APPLICATIONS_URL + pk, json)
    return data.json(), data.status_code


# CLC Queries
def put_clc_queries(request, pk, json):
    data = put(request, CLC_QUERIES_URL + pk, json)
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
    data = get(request, CASE_URL + pk + ACTIVITY_URL + '?fields=status,flags')
    return data.json(), data.status_code


# Case Documents
def get_case_document(request, pk, s3_key):
    data = get(request, CASE_URL + pk + DOCUMENTS_URL + s3_key)
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
def get_case_advice(request, case_pk):
    data = get(request, CASE_URL + case_pk + ADVICE_URL)
    return data.json(), data.status_code


def post_case_advice(request, case_pk, json):
    import ast

    def _clean_dict_item(item):
        return ast.literal_eval(item)

    json = json.copy()

    json['goods'] = _clean_dict_item(json['goods'])
    json['goods_types'] = _clean_dict_item(json['goods_types'])
    json['countries'] = _clean_dict_item(json['countries'])
    json['end_user'] = _clean_dict_item(json['end_user'])
    json['ultimate_end_users'] = _clean_dict_item(json['ultimate_end_users'])
    json['denial_reasons'] = json.getlist('denial_reasons')

    if json['end_user']:
        json['end_user'] = json['end_user'][0]
    else:
        json['end_user'] = None

    print(json)

    data = post(request, CASE_URL + case_pk + ADVICE_URL, json)
    return data.json(), data.status_code
