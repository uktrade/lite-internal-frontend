from typing import List, Dict

from cases.objects import Case


def get_destinations(request, case: Case):
    selected_destinations_ids = [*request.GET.getlist("destinations"), *request.GET.getlist("countries")]
    destinations = case.destinations
    return_values = []

    for destination in destinations:
        if destination["id"] in selected_destinations_ids:
            return_values.append(destination)

    return return_values


def get_goods(request, case: Case):
    selected_goods_ids = request.GET.getlist("goods", request.GET.getlist("goods_types"))
    goods = case.data.get("goods", case.data.get("goods_types"))
    return_values = []

    for good in goods:
        if "good" in good:
            if good["good"]["id"] in selected_goods_ids:
                return_values.append(good)
        else:
            if good["id"] in selected_goods_ids:
                return_values.append(good)

    return return_values


def flatten_advice_data(request, items: List[Dict]):
    if not items or not items[0].get("advice"):
        return

    first_item_advice = items[0]["advice"][0]
    keys = ["proviso", "denial_reasons", "note", "text", "type"]

    for item in items:
        for advice in [
            advice for advice in item.get("advice", []) if advice["user"]["id"] == request.user.lite_api_user_id
        ]:
            for key in keys:
                if advice[key] != first_item_advice[key]:
                    return

    return first_item_advice
