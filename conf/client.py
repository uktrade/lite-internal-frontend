import requests

from conf.settings import env


def get(request, appended_address):
    if request:
        return requests.get(env("LITE_API_URL") + appended_address,
                            headers={'GOV-USER-EMAIL': str(request.user.email)})

    return requests.get(env("LITE_API_URL") + appended_address)


def post(request, appended_address, json):
    if request:
        return requests.post(env("LITE_API_URL") + appended_address,
                             json=json,
                             headers={'GOV-USER-EMAIL': str(request.user.email)})

    return requests.post(env("LITE_API_URL") + appended_address,
                         json=json)


def put(request, appended_address, json):
    return requests.put(env("LITE_API_URL") + appended_address,
                        json=json,
                        headers={'GOV-USER-EMAIL': str(request.user.email)})


def delete(request, appended_address):
    return requests.delete(env("LITE_API_URL") + appended_address,
                           headers={'GOV-USER-EMAIL': str(request.user.email)})
