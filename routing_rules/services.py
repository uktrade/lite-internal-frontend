from conf.client import get, post, put
from conf.constants import ROUTING_RULES_URL, ROUTING_RULES_STATUS_URL


def get_routing_rules(request, params=""):
    data = get(request, ROUTING_RULES_URL + "?" + params)
    return data.json(), data.status_code


def get_routing_rule(request, id):
    data = get(request, ROUTING_RULES_URL + str(id))
    return data.json(), data.status_code


def _remove_none_from_checkbox(json):
    data = json
    additional_rules = json.get("additional_rules", None)
    if "None" in additional_rules:
        new_additional_rules = []
        for rule in additional_rules:
            if rule != "None":
                new_additional_rules.append(rule)
        data["additional_rules"] = new_additional_rules

    return data


def post_routing_rule(request, json):
    data = _remove_none_from_checkbox(json)
    response = post(request, ROUTING_RULES_URL, data)
    return response.json(), response.status_code


def validate_put_routing_rule(request, id, json):
    data = json
    data["validate_only"] = True
    return put_routing_rule(request, id, data)


def put_routing_rule(request, id, json):
    data = _remove_none_from_checkbox(json)
    response = put(request, ROUTING_RULES_URL + str(id), data)
    return response.json(), response.status_code


def put_routing_rule_active_status(request, id, json):
    data = put(request, ROUTING_RULES_URL + str(id) + ROUTING_RULES_STATUS_URL, json)
    return data.json(), data.status_code
