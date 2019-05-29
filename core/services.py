from conf.client import get
from conf.constants import DENIAL_REASONS_URL
from libraries.forms.components import Option


def get_denial_reasons(request):
    data = get(request, DENIAL_REASONS_URL).json()
    converted = []

    for denial_reason in data.get('denial_reasons'):
        converted.append(
           Option(denial_reason['id'], denial_reason['id'])
        )

    return converted
