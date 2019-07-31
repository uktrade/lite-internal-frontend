from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from flags.forms import edit_flag_form
from libraries.forms.generators import form_page
from picklists.forms import add_picklist_item_form
from django.shortcuts import render, redirect
from picklists.services import get_picklists, get_picklist_item, post_picklist_item


class Picklists(TemplateView):

    def get(self, request, **kwargs):
        picklist_items, status_code = get_picklists(request)
        # picklist_items, status_code = get_gov_user(request, str(request.user.lite_api_user_id))

        context = {
            'title': 'Picklists',
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
        # data, status_code = get_flag(request, str(kwargs['pk']))
        return form_page(request, edit_flag_form())
