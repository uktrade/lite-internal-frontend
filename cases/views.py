import requests

from django.shortcuts import render

from conf.settings import env
from django.shortcuts import render
from django.views.generic import TemplateView


def index(request):
    queue_id = request.GET.get('queue')

    # If a queue id is not provided, use the default queue
    if not queue_id:
        queue_id = '00000000-0000-0000-0000-000000000001'

    queues = requests.get(env("LITE_API_URL") + '/queues/').json()
    response = requests.get(env("LITE_API_URL") + '/queues/' + queue_id + '/').json()

    context = {
        'queues': queues,
        'queue_id': queue_id,
        'data': response,
        'title': response.get('queue').get('name'),
    }
    return render(request, 'cases/index.html', context)


def case(request, pk):
    response = requests.get(env("LITE_API_URL") + '/cases/' + str(pk) + '/').json()

    context = {
        'data': response,
        'title': response.get('case').get('application').get('name'),
    }
    return render(request, 'cases/case.html', context)


class ManageCase(TemplateView):
    def get(self, request, pk):
        response = requests.get(env("LITE_API_URL") + '/cases/' + str(pk) + '/').json()
        context = {
          'data': response,
          'title': 'Manage ' + response.get('case').get('application').get('name'),
        }
        return render(request, 'cases/manage.html', context)
