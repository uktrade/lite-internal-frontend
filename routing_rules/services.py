from conf.client import get, post, put
from conf.constants import ROUTING_RULES_URL, ROUTING_RULES_STATUS_URL


def get_routing_rules(request, params=""):
    data = get(request, ROUTING_RULES_URL + "?" + params)
    return data.json(), data.status_code


def get_routing_rule():
    pass


def post_routing_rule(request, json):
    data = post(request, ROUTING_RULES_URL, json)
    return data.json(), data.status_code


def put_routing_rule():
    pass


def put_routing_rule_status(request, id, status):
    data = put(request, ROUTING_RULES_URL + id + ROUTING_RULES_STATUS_URL + status, {})
    return data.json(), data.status_code
