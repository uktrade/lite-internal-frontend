from conf.client import get, post, put
from conf.constants import PICKLIST_URL, LETTER_TEMPLATES_URL


def get_letter_paragraphs(request, ids: list):
    if not ids:
        return []

    data = get(request, PICKLIST_URL + '?type=letter_paragraph' + '&ids=' + ','.join(ids))
    return data.json()['picklist_items']


def get_letter_template(request, pk):
    data = get(request, LETTER_TEMPLATES_URL + pk)
    return data.json()


def put_letter_template(request, pk, json):
    data = put(request, LETTER_TEMPLATES_URL + pk, json)
    return data.json(), data.status_code


def get_letter_templates(request):
    data = get(request, LETTER_TEMPLATES_URL)
    return data.json()['results']


def post_letter_template(request, json):
    data = post(request, LETTER_TEMPLATES_URL, json)
    return data.json(), data.status_code
