from conf.client import post, get, put
from conf.constants import CASE_URL, CASE_NOTES_URL, APPLICATIONS_URL, ACTIVITY_URL, DOCUMENTS_URL


def get_case(request, pk):
    data = get(request, CASE_URL + pk)
    return data.json(), data.status_code


def put_case(request, pk, json):
    data = put(request, CASE_URL + pk + '/', json)
    return data.json(), data.status_code


# Applications


def put_applications(request, pk, json):
    data = put(request, APPLICATIONS_URL + pk + '/', json)
    return data.json(), data.status_code


# Case Notes


def get_case_notes(request, pk):
    data = get(request, CASE_URL + pk + CASE_NOTES_URL)
    return data.json(), data.status_code


def post_case_notes(request, pk, json):
    data = post(request, CASE_URL + pk + CASE_NOTES_URL, json)
    return data.json(), data.status_code


# Activity


def get_activity(request, pk):
    data = get(request, CASE_URL + pk + ACTIVITY_URL + '?fields=status')
    return data.json(), data.status_code


# Case Documents


def get_case_documents(request, pk):
    data = get(request, CASE_URL + pk + DOCUMENTS_URL)
    return data.json(), data.status_code


def post_case_documents(request, pk, json):
    data = post(request, CASE_URL + pk + DOCUMENTS_URL, json)
    return data.json(), data.status_code
