import json

from conf.client import get, post, put
from conf.constants import QUEUES_URL
from libraries.forms.components import Option


def get_queues(request, convert_to_options=False):
    data = get(request, QUEUES_URL)

    if convert_to_options:
        converted = []

        for queue in data.json().get('queues'):
            converted.append(
                Option(queue.get('id'), queue.get('name'), description=queue.get('team').get('name'))
            )

        return converted

    return data.json(), data.status_code


def post_queues(request, json):
    data = post(request, QUEUES_URL, json)
    return data.json(), data.status_code


def get_queue(request, pk, filter=None, sort=None):
    filter_and_sort = []

    if filter:
        # filter = json.dumps()
        filter_and_sort.append('filter=' + filter)

    if sort:
        sort_json = sort.split('-')
        if len(sort_json) == 2:
            sort = json.dumps({sort_json[0]: sort_json[1]})
            filter_and_sort.append('sort=' + sort)

    filter_and_sort = '?' + '&'.join(filter_and_sort) if len(filter_and_sort) > 0 else ''

    data = get(request, QUEUES_URL + pk + filter_and_sort)

    return data.json(), data.status_code


def put_queue(request, pk, json):
    data = put(request, QUEUES_URL + pk + '/', json)
    return data.json(), data.status_code


# Case Assignments


def get_queue_case_assignments(request, pk):
    data = get(request, QUEUES_URL + pk + '/case-assignments/')
    return data.json(), data.status_code


def put_queue_case_assignments(request, pk, json):
    data = put(request, QUEUES_URL + pk + '/case-assignments/', json)
    return data.json(), data.status_code

