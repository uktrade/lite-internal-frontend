import requests

from django.shortcuts import render

import libraries.jsondate as jsondate

from conf.settings import env


def cases(request):
    response = requests.get(env("LITE_API_URL") + '/cases')
    context = {
        #'data': jsondate.loads(response.text),
        'title': 'Cases',
    }
    return render(request, 'cases/index.html', context)
