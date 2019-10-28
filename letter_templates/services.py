from conf.client import get, post, put
from conf.constants import PICKLIST_URL, LETTER_TEMPLATES_URL


def sort_letter_paragraphs(paragraphs, ids):
    """Order a list of letter paragraphs in the same order as a list of IDs."""
    paragraphs_by_id = {p["id"]: p for p in paragraphs}
    return [paragraphs_by_id[id] for id in ids if id in paragraphs_by_id]


def get_letter_paragraphs(request, ids: list):
    if not ids:
        return []

    data = get(request, PICKLIST_URL + '?type=letter_paragraph' + '&ids=' + ','.join(ids))
    letter_paragraphs = data.json()['picklist_items']
    letter_paragraphs = sort_letter_paragraphs(letter_paragraphs, ids)
    return letter_paragraphs


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
