from cases.forms.assign_users import assign_users_form
from cases.services import get_case, put_case
from libraries.forms.generators import error_page, form_page
from queues.services import get_queue, get_queues, \
    post_queues, put_queue
from queues import forms

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from users.services import get_gov_user


class QueuesList(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_queues(request)
        user_data, status_code = get_gov_user(request, str(request.user.user_token))

        context = {
            'data': data,
            'title': 'Queues',
            'user_data': user_data,
        }
        return render(request, 'queues/index.html', context)


class AddQueue(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': 'Add Queue',
            'page': forms.form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        # including the user's team details in the post request
        user_data, status_code = get_gov_user(request, str(request.user.user_token))
        post_data = request.POST.copy()
        post_data['team'] = user_data['user']['team']
        data, status_code = post_queues(request, post_data)

        if status_code == 400:
            context = {
                'title': 'Add Queue',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('queues:queues'))


class EditQueue(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_queue(request, str(kwargs['pk']))
        context = {
            'data': data.get('queue'),
            'title': 'Edit Queue',
            'page': forms.edit_form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data, status_code = put_queue(request, str(kwargs['pk']), request.POST)
        if status_code == 400:
            context = {
                'title': 'Add Queue',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('queues:queues'))


class CaseAssignments(TemplateView):
    def get(self, request, **kwargs):
        case_ids = request.GET.get('cases').split(',')
        user_data, status_code = get_gov_user(request, str(request.user.user_token))

        if not request.GET.get('cases'):
            return error_page(request, 'Invalid case selection')

        for case_id in case_ids:
            case, status_code = get_case(request, case_id)

        return form_page(request, assign_users_form(request,
                                                    user_data['user']['team'],
                                                    len(case_ids) > 1),
                         data=case['case'])

    def post(self, request, **kwargs):
        case_ids = request.GET.get('cases').split(',')
        user_data, status_code = get_gov_user(request, str(request.user.user_token))

        data = {
            'users': request.POST.getlist('users'),
        }

        for case_id in case_ids:
            response, status_code = put_case(request, case_id, data)

            if 'errors' in response:
                return form_page(request, assign_users_form(request,
                                                            user_data['user']['team'],
                                                            len(case_ids) > 1),
                                 data=request.POST,
                                 errors=response['errors'])

        # If there is no response (no forms left to go through), go to the case page
        return redirect(reverse('cases:cases'))
