import json
import requests
from django.contrib.auth.models import AnonymousUser
from mohawk import Sender

from conf.settings import env


def get(request, appended_address):
    url = env("LITE_API_URL") + appended_address

    # If a URL doesn't end with a slash and doesn't have URL parameter, add the trailing slash
    if not url.endswith("/") and "?" not in url:
        url = url + "/"

    sender = _get_hawk_sender(url, "GET", "text/plain", {})

    if request:
        response = requests.get(url, headers=_get_headers(request, sender),)

        _verify_api_response(response, sender)

        return response

    return requests.get(url)


def post(request, appended_address, request_data):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    url = env("LITE_API_URL") + appended_address

    if request:
        sender = _get_hawk_sender(url, "POST", "application/json", json.dumps(request_data))

        response = requests.post(url, json=request_data, headers=_get_headers(request, sender),)

        _verify_api_response(response, sender)

        return response
    else:
        # Staff SSO requests aren't signed and responses aren't verified
        return requests.post(url, json=request_data)


def put(request, appended_address: str, request_data):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    url = env("LITE_API_URL") + appended_address

    sender = _get_hawk_sender(url, "PUT", "application/json", json.dumps(request_data))

    response = requests.put(url, json=request_data, headers=_get_headers(request, sender),)

    _verify_api_response(response, sender)

    return response


def patch(request, appended_address: str, request_data):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    url = env("LITE_API_URL") + appended_address

    sender = _get_hawk_sender(url, "PATCH", "application/json", json.dumps(request_data))

    response = requests.patch(
        url=env("LITE_API_URL") + appended_address, json=request_data, headers=_get_headers(request, sender),
    )

    _verify_api_response(response, sender)

    return response


def delete(request, appended_address):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    url = env("LITE_API_URL") + appended_address

    sender = _get_hawk_sender(url, "DELETE", "text/plain", {})

    response = requests.delete(url=env("LITE_API_URL") + appended_address, headers=_get_headers(request, sender),)

    _verify_api_response(response, sender)

    return response


def _get_headers(request, sender: Sender):
    headers = {
        "X-Correlation-Id": str(request.correlation),
        "Authorization": sender.request_header,
    }

    if not isinstance(request.user, AnonymousUser):
        headers["GOV-USER-TOKEN"] = str(request.user.user_token)

    return headers


def _get_hawk_sender(url: str, method: str, content_type: str, content):
    return Sender(
        {"id": "internal-frontend", "key": env("LITE_API_HAWK_KEY"), "algorithm": "sha256"},
        url,
        method,
        content=content,
        content_type=content_type,
    )


def _verify_api_response(response, sender: Sender):
    sender.accept_response(
        response.headers["server-authorization"],
        content=response.content,
        content_type=response.headers["Content-Type"],
    )
