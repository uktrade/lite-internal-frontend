import requests

from django.shortcuts import render
from django.views.generic import TemplateView

from conf.settings import env
from organisations.services import get_organisations


class OrganisationList(TemplateView):

    def get(self, request, **kwargs):
        data, status_code = get_organisations(request)
        context = {
            'data': data,
            'title': 'Organisations',
        }
        return render(request, 'organisations/index.html', context)


class OrganisationDetail(TemplateView):

    def get(self, request, **kwargs):
        response = requests.get(env("LITE_API_URL") + '/organisations/' + kwargs['pk'] + '/').json()
        context = {
            'data': response,
            'title': response['organisation']['name'],
        }
        return render(request, 'organisations/organisation.html', context)
