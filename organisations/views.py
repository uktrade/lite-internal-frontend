import requests

from django.shortcuts import render

import libraries.jsondate as jsondate

from conf.settings import env


def show_orgs(request):
    response = requests.get(env("LITE_API_URL") + '/organisations')

    print(response.text)

    context = {
        'data': jsondate.loads(response.text),
        'title': 'Organisations',
    }

    # context = {
    #     'title': 'List of Registered Organizations',
    # }
    return render(request, 'organisations/index.html', context)
