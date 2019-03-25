from django.shortcuts import render, redirect
import requests
import libraries.jsondate as json
from conf.settings import env
from django.urls import reverse_lazy


def show_orgs(request):
    context = {
        'title': 'List of Registered Organizations',
    }
    return render(request, 'organisations/index.html', context)
