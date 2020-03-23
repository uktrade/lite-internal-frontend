from conf.client import get, post, put
from conf.constants import ORGANISATIONS_URL, SITES_URL, USERS_URL


def get_organisations(request, params):
    data = get(request, ORGANISATIONS_URL + "?" + params)
    return data.json(), data.status_code


def post_organisations(request, json):
    data = post(request, ORGANISATIONS_URL, json)
    return data.json(), data.status_code


def put_organisation(request, pk, json):
    if "status" in json:
        del json["status"]
    data = put(request=request, appended_address=ORGANISATIONS_URL + str(pk) + "/", json=json)
    return data.json(), data.status_code


def validate_post_organisation(request, pk, json):
    json = json.copy()
    json["validate_only"] = True

    data = put(request=request, appended_address=ORGANISATIONS_URL + str(pk) + "/", json=json)
    return data.json(), data.status_code


def get_organisation(request, pk):
    data = get(request, ORGANISATIONS_URL + str(pk))
    return data.json()


def get_organisation_sites(request, pk):
    data = get(request, ORGANISATIONS_URL + str(pk) + SITES_URL + "?disable_pagination=True")
    return data.json()["sites"]


def get_organisation_members(request, pk):
    data = get(request, ORGANISATIONS_URL + str(pk) + USERS_URL + "?disable_pagination=True")
    return data.json()
