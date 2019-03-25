from django.shortcuts import render
import requests
from register_business import forms
from django.http import Http404
from conf.settings import env
import json


def register(request):
    context = {
        'page': forms.section1.forms[0],
    }
    return render(request, 'register_business/form.html', context)


def submit(request):
    response = requests.post(env("LITE_API_URL") + '/organisations/')
    data = json.loads(response.text)

    if 'errors' in data:
        raise Http404

    context = {
        'title': 'Organisation Submitted',
        'data': data
    }
    return render(request, 'register_business/registration_success.html', context)
