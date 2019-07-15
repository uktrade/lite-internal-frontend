from django.shortcuts import render
from django.views.generic import TemplateView

from core.builtins.custom_tags import get_string
from libraries.forms.generators import form_page
from users.forms.roles import add_role


class Roles(TemplateView):
    def get(self, request, **kwargs):
        # roles, status_code = get_roles(request)
        # permissions, status_code = get_permissions(request)

        roles = {
            'roles': [
                {
                    'id': '123',
                    'name': 'Admin',
                    'permissions': [
                        '123',
                    ]
                }
            ]
        }
        all_permissions = {
            'permissions': [
                {
                    'id': '123',
                    'name': 'Make final decisions'
                },
                {
                    'id': '1234',
                    'name': 'Ban users'
                },
                {
                    'id': '12345',
                    'name': 'Create queues'
                }
            ]
        }

        context = {
            'all_permissions': all_permissions['permissions'],
            'roles': roles['roles'],
            'title': get_string('roles.title'),
        }
        return render(request, 'users/roles.html', context)


class AddRole(TemplateView):

    form = add_role()

    def get(self, request, **kwargs):
        # roles, status_code = get_roles(request)
        # permissions, status_code = get_permissions(request)

        # all_permissions = {
        #     'permissions': [
        #         {
        #             'id': '123',
        #             'name': 'Make final decisions'
        #         },
        #         {
        #             'id': '1234',
        #             'name': 'Ban users'
        #         },
        #         {
        #             'id': '12345',
        #             'name': 'Create queues'
        #         }
        #     ]
        # }

        # context = {
        #     'title': get_string('roles.add.title'),
        # }
        return form_page(request, self.form)
