from conf.client import get
from conf.constants import LETTER_TEMPLATES_URL


def get_letter_templates(request):
    data = get(request, LETTER_TEMPLATES_URL)
    return data.json()['letter_templates']
