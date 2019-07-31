from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from libraries.forms.generators import form_page
from picklists.forms import add_picklist_item_form
from picklists.services import post_picklist_item
from django.shortcuts import render, redirect
from picklists.services import get_picklists
from users.services import get_gov_user


class Picklists(TemplateView):

    def get(self, request, **kwargs):
        # data, status_code = get_picklists(request)
        # picklist_items, status_code = get_gov_user(request, str(request.user.lite_api_user_id))

        context = {
            'title': 'Pick List',
            'picklist_items': [
                {
                    'id': '123',
                    'team': '123',
                    'name': 'my pick list item!!',
                    'text': '590000sdifjkn dskjfnskd,f jksdn jkfgndcjkaws vdf',
                    'type': 'Provisio',
                    'status': 'Activated'
                },
                {
                    'id': '123',
                    'team': '123',
                    'name': 'my pick list item!!',
                    'text': '590000sdifjkn dskjfnskd,f jksdn jkfgndcjkaws vdf',
                    'type': 'Provisio',
                    'status': 'Activated'
                },
                {
                    'id': '123',
                    'team': '123',
                    'name': 'my pick list item!!',
                    'text': '590000sdifjkn dskjfnskd,f jksdn jkfgndcjkaws vdf',
                    'type': 'Provisio',
                    'status': 'Activated'
                },
                {
                    'id': '123',
                    'team': '123',
                    'name': 'my pick list item!!',
                    'text': '590000sdifjkn dskjfnskd,f jksdn jkfgndcjkaws vdf',
                    'type': 'Provisio',
                    'status': 'Activated'
                }
            ],
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


# class EditFlag(TemplateView):
#     def get(self, request, **kwargs):
#         data, status_code = get_flag(request, str(kwargs['pk']))
#         return form_page(request, edit_flag_form(), data=data['flag'])
#
#     def post(self, request, **kwargs):
#         response, status_code = put_flag(request, str(kwargs['pk']), request.POST)
#         if status_code != 200:
#             return form_page(request, edit_flag_form(), data=request.POST, errors=response.get('errors'))
#
#         return redirect(reverse_lazy('flags:flags'))
#
#
# class ViewFlag(TemplateView):
#     def get(self, request, **kwargs):
#         data, status_code = get_flag(request, str(kwargs['pk']))
#
#         context = {
#             'data': data,
#             'title': data['flag']['name']
#         }
#         return render(request, 'flags/profile.html', context)