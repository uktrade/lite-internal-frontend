from django.shortcuts import render

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
        data = request.POST

        form = get_next_form_after_pk(data.get('form_pk'), forms.register_business_forms)

        context = {
            'page': form,
            'title': form.title,
        }
        return render(request, 'form.html', context)
