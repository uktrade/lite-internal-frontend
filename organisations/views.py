from django.shortcuts import render, redirect
import requests
from form import forms
import libraries.jsondate as json
from conf.settings import env
from django.urls import reverse_lazy


def show_orgs(request):
    context = {
        'title': 'List of Registered Organizations',
    }
    return render(request, 'organisations/index.html', context)


def form(request):
    return render(request, 'organisations/form.html')