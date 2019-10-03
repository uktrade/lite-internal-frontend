from conf.client import get
from conf.constants import PICKLIST_URL


def get_letter_paragraphs(request, ids: list):
    if not ids:
        return []

    if not isinstance(ids, list):
        ids = [ids]
    data = get(request, PICKLIST_URL + '?type=letter_paragraph' + '&ids=' + ','.join(ids))
    return data.json()['picklist_items']
