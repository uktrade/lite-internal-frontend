from django.shortcuts import render
from django.views.generic import TemplateView

from flags.forms import edit_flag_form
from libraries.forms.generators import form_page
from picklists.forms import add_picklist_item_form
from picklists.services import get_picklists
from users.services import get_gov_user


class Picklists(TemplateView):

    def get(self, request, **kwargs):
        # data, status_code = get_picklists(request)
        # picklist_items, status_code = get_gov_user(request, str(request.user.lite_api_user_id))

        context = {
            'title': 'Picklists',
            'picklist_items': [
                {
                    'id': '84401e06-4e23-41b8-bd1b-cfab21a2d977',
                    'team': '84401e06-4e23-41b8-bd1b-cfab21a2d977',
                    'name': 'my pick list item!!',
                    'text': '590000sdifjkn dskjfnskd,f jksdn jkfgndcjkaws vdf',
                    'type': 'Provisio',
                    'status': 'Activated'
                },
                {
                    'id': '84401e06-4e23-41b8-bd1b-cfab21a2d977',
                    'team': '84401e06-4e23-41b8-bd1b-cfab21a2d977',
                    'name': 'my pick list item!!',
                    'text': '590000sdifjkn dskjfnskd,f jksdn jkfgndcjkaws vdf',
                    'type': 'Provisio',
                    'status': 'Activated'
                },
                {
                    'id': '84401e06-4e23-41b8-bd1b-cfab21a2d977',
                    'team': '84401e06-4e23-41b8-bd1b-cfab21a2d977',
                    'name': 'my pick list item!!',
                    'text': '590000sdifjkn dskjfnskd,f jksdn jkfgndcjkaws vdf',
                    'type': 'Provisio',
                    'status': 'Activated'
                },
                {
                    'id': '84401e06-4e23-41b8-bd1b-cfab21a2d977',
                    'team': '84401e06-4e23-41b8-bd1b-cfab21a2d977',
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

    # def post(self, request, **kwargs):
    #     response, status_code = post_flags(request, request.POST)
    #     if status_code != 201:
    #         return form_page(request, add_flag_form(), data=request.POST, errors=response.get('errors'))
    #
    #     return redirect(reverse_lazy('flags:flags'))


class PicklistItem(TemplateView):
    def get(self, request, **kwargs):
        # data, status_code = get_flag(request, str(kwargs['pk']))

        data = {
                   'id': '84401e06-4e23-41b8-bd1b-cfab21a2d977',
                   'team': '84401e06-4e23-41b8-bd1b-cfab21a2d977',
                   'name': 'my pick list item!!',
                   'text': '590000sdifjkn dskjfnskd,f jksdn jkfgndcjkaws vdf',
                   'type': 'Provisio',
                   'status': 'Activated'
               }

        context = {
            'title': 'Picklist item!',
            'picklist_item': data,
        }
        return render(request, 'teams/picklist-item.html', context)


class EditPicklistItem(TemplateView):
    def get(self, request, **kwargs):
        # data, status_code = get_flag(request, str(kwargs['pk']))
        return form_page(request, edit_flag_form())
