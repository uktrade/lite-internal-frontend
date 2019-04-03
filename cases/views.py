import requests

from django.shortcuts import render

from conf.settings import env


def index(request):
    queue_id = request.GET.get('queue')

    if not queue_id:
        queue_id = '00000000-0000-0000-0000-000000000000'

    queues = requests.get(env("LITE_API_URL") + '/queues/')
    response = requests.get(env("LITE_API_URL") + '/queues/' + queue_id + '/')

    context = {
        'queues': queues.json(),
        'queue_id': queue_id,
        'data': response.json(),
        'title': response.json()['queue']['name'],
    }
    return render(request, 'cases/index.html', context)


def case(request, pk):
    response = requests.get(env("LITE_API_URL") + '/cases/' + str(pk) + '/')
    data = response.json()

    context = {
        'data': data,
        'title': data.get("case").get("application").get("name"),
    }
    return render(request, 'cases/case.html', context)
