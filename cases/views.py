import requests

from django.shortcuts import render

import libraries.jsondate as jsondate

from conf.settings import env


def index(request):
    queue_id = request.GET.get('queue')

    if not queue_id:
        queue_id = '00000000-0000-0000-0000-000000000000'

    queues = requests.get(env("LITE_API_URL") + '/queues/')
    response = requests.get(env("LITE_API_URL") + '/queues/' + queue_id + '/')

    context = {
        'queues': jsondate.loads(queues.text),
        'queue_id': queue_id,
        'data': jsondate.loads(response.text),
        'title': 'Cases',
    }
    return render(request, 'cases/index.html', context)


def case(request, pk):
    response = requests.get(env("LITE_API_URL") + '/cases/' + str(pk) + '/')
    data = jsondate.loads(response.text)

    context = {
        'data': data,
        'title': data.get("case").get("application").get("name"),
    }
    return render(request, 'cases/case.html', context)
