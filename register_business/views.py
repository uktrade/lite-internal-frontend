from django.shortcuts import render

from libraries.forms.components import HiddenField
from libraries.forms.helpers import get_next_form_after_pk
from register_business import forms


def register(request):
    if request.method == 'GET':
        context = {
            'page': forms.register_business_forms.forms[0],
            'title': forms.register_business_forms.forms[0].title,
        }
        return render(request, 'form.html', context)

    elif request.method == 'POST':
        data = request.POST.copy()

        # Get the next form based off form_pk
        form = get_next_form_after_pk(data.get('form_pk'), forms.register_business_forms)

        # Remove form_pk and CSRF from POST data as the new form will replace them
        del data['form_pk']
        del data['csrfmiddlewaretoken']

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
