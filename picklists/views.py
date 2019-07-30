from django.shortcuts import render
from django.views.generic import TemplateView

from picklists.services import get_picklists
from users.services import get_gov_user


class Picklist(TemplateView):

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
                    }
                ],
        }
        return render(request, 'teams/picklist.html', context)


# class AddFlag(TemplateView):
#     def get(self, request, **kwargs):
#         return form_page(request, add_flag_form())
#
#     def post(self, request, **kwargs):
#         response, status_code = post_flags(request, request.POST)
#         if status_code != 201:
#             return form_page(request, add_flag_form(), data=request.POST, errors=response.get('errors'))
#
#         return redirect(reverse_lazy('flags:flags'))
#
#
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
#
#
# class ChangeFlagStatus(TemplateView):
#     def get(self, request, **kwargs):
#         status = kwargs['status']
#         description = ''
#
#         if status != 'deactivate' and status != 'reactivate':
#             raise Http404
#
#         if status == 'deactivate':
#             description = get_string('flags.update_flag.status.deactivate_warning')
#
#         if status == 'reactivate':
#             description = get_string('flags.update_flag.status.reactivate_warning')
#
#         context = {
#             'title': 'Are you sure you want to {} this flag?'.format(status),
#             'description': description,
#             'user_id': str(kwargs['pk']),
#             'status': status,
#         }
#         return render(request, 'flags/change_status.html', context)
#
#     def post(self, request, **kwargs):
#         status = kwargs['status']
#
#         if status != 'deactivate' and status != 'reactivate':
#             raise Http404
#
#         put_flag(request, str(kwargs['pk']), json={'status': request.POST['status']})
#
#         return redirect(reverse_lazy('flags:flags'))
#
