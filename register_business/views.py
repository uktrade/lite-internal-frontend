import json

from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from conf.client import post
from libraries.forms.components import HiddenField
from libraries.forms.helpers import get_next_form_after_pk, nest_data, get_form_by_pk
from register_business import forms


class RegisterBusiness(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'page': forms.register_business_forms.forms[0],
            'title': forms.register_business_forms.forms[0].title,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data = request.POST.copy()

        # Get the next form based off form_pk
        current_form = get_form_by_pk(data.get('form_pk'), forms.register_business_forms)
        form = get_next_form_after_pk(data.get('form_pk'), forms.register_business_forms)

        # Remove form_pk and CSRF from POST data as the new form will replace them
        del data['form_pk']
        del data['csrfmiddlewaretoken']

        # Post the data to the validator and check for errors
        nested_data = nest_data(data)

        validated_data = post(request, '/organisations/validate/', nested_data).json()

        if 'errors' in validated_data:
            context = {
                'page': current_form,
                'title': current_form.title,
                'errors': validated_data['errors'].get(current_form.prefix),
                'data': data,
            }
            return render(request, 'form.html', context)

        # If there aren't any forms left to go through, submit all the data
        if form is None:
            validated_data = post(request, '/organisations/', nested_data).json()

            if 'errors' in validated_data:
                context = {
                    'page': current_form,
                    'title': current_form.title,
                    'errors': validated_data['errors'].get(current_form.prefix),
                    'data': data,
                }
                return render(request, 'form.html', context)

            return redirect('/organisations/')

        # Add existing post data to new form as hidden fields
        for key, value in data.items():
            form.questions.append(
                HiddenField(key, value)
            )

        context = {
            'page': form,
            'title': form.title,
        }
        return render(request, 'form.html', context)
