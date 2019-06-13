from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from users import forms
from users.services import get_users, post_users, update_user, get_user


class UsersList(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_users(request)

        context = {
            'data': data,
            'title': 'Users',
        }
        return render(request, 'users/index.html', context)


class AddUser(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': 'Add User',
            'page': forms.form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data, status_code = post_users(request, request.POST)

        if status_code == 400:
            context = {
                'title': 'Add User',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('users:users'))


class ViewUser(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_user(request, str(kwargs['pk']))
        user = data.get('user')

        context = {
            'data': data,
            'title': user.get('first_name') + ' ' + user.get('last_name')
        }
        return render(request, 'users/profile.html', context)


class ViewProfile(TemplateView):
    def get(self, request, **kwargs):
        user = request.user
        return redirect(reverse_lazy('users:user', kwargs={'pk': user.id}))


class EditUser(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_user(request, str(kwargs['pk']))
        context = {
            'data': data.get('user'),
            'title': 'Edit User',
            'page': forms.edit_form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data, status_code = update_user(request, str(kwargs['pk']), request.POST)
        if status_code == 400:
            context = {
                'title': 'Add User',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('users:user', kwargs={'pk': str(kwargs['pk'])}))


class ChangeUserStatus(TemplateView):
    def get(self, request, **kwargs):
        status = kwargs['status']
        description = ''

        if status != 'deactivate' and status != 'reactivate':
            raise Http404

        if status == 'deactivate':
            description = 'This user will no longer be able to log in or perform tasks on LITE ' \
                          'on behalf of your organisation.'

        if status == 'reactivate':
            description = 'This user will be able to log in to and perform tasks on LITE on behalf ' \
                          'of your organisation.'

        context = {
            'title': 'Are you sure you want to {} this user?'.format(status),
            'description': description,
            'user_id': str(kwargs['pk']),
            'status': status,
        }
        return render(request, 'users/change_status.html', context)

    def post(self, request, **kwargs):
        status = kwargs['status']

        if status != 'deactivate' and status != 'reactivate':
            raise Http404

        update_user(request, str(kwargs['pk']), json={'status': request.POST['status']})

        return redirect('/users/')
