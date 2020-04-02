from conf.client import get, post
from conf.constants import ROUTING_RULES_URL


def get_routing_rules(request):
    data = get(request, ROUTING_RULES_URL)
    return data.json(), data.status_code


def get_routing_rule():
    pass


def post_routing_rule(request, json):
    data = post(request, ROUTING_RULES_URL, json)
    return data.json(), data.status_code


def put_routing_rule():
    pass
