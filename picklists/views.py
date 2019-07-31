from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from libraries.forms.generators import form_page
from picklists.forms import add_picklist_item_form, edit_picklist_item_form
from picklists.services import get_picklists, get_picklist_item, post_picklist_item, put_picklist_item
from teams.services import get_team
from users.services import get_gov_user


class Picklists(TemplateView):

    def get(self, request, **kwargs):
        # Ensure that the page has a type
        picklist_type = request.GET.get('type')
        if not picklist_type:
            return redirect(reverse_lazy('picklists:picklists') + '?type=proviso')

        user, status_code = get_gov_user(request)
        team, status_code = get_team(request, user['user']['team']['id'])
        # Get picklist items depending on the type given
        picklist_items, status_code = get_picklists(request, picklist_type)

        context = {
            'title': 'Picklists - ' + team['team']['name'],
            'team': team['team'],
            'picklist_items': picklist_items['picklist_items'],
        }
        return render(request, 'teams/picklist.html', context)


class AddPicklistItem(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, add_picklist_item_form())

    def post(self, request, **kwargs):
        response, status_code = post_picklist_item(request, request.POST)

        if status_code != 201:
            return form_page(request, add_picklist_item_form(), data=request.POST, errors=response.get('errors'))

        return redirect(reverse_lazy('picklists:picklists'))


class ViewPicklistItem(TemplateView):
    def get(self, request, **kwargs):
        picklist_item, status_code = get_picklist_item(request, str(kwargs['pk']))

        context = {
            'title': picklist_item['picklist_item']['name'],
            'picklist_item': picklist_item['picklist_item'],
        }
        return render(request, 'teams/picklist-item.html', context)


class EditPicklistItem(TemplateView):
    def get(self, request, **kwargs):
        picklist_item, status_code = get_picklist_item(request, str(kwargs['pk']))
        return form_page(request, edit_picklist_item_form(), data=picklist_item['picklist_item'])

    def post(self, request, **kwargs):
        response, status_code = put_picklist_item(request, str(kwargs['pk']), request.POST)
        if status_code != 200:
            return form_page(request, edit_picklist_item_form(), data=request.POST, errors=response.get('errors'))

        return redirect(reverse_lazy('picklists:picklists'))
