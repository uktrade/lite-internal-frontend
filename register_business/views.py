import json

from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from libraries.forms.components import HiddenField
from libraries.forms.helpers import get_next_form_after_pk, nest_data
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
        form = get_next_form_after_pk(data.get('form_pk'), forms.register_business_forms)

        # Remove form_pk and CSRF from POST data as the new form will replace them
        del data['form_pk']
        del data['csrfmiddlewaretoken']

        # If there aren't any forms left to go through, submit all the data
        if form is None:
            print(json.dumps(nest_data(data)))
            return redirect('/')

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
