from django.shortcuts import render

from register_business import forms


def register(request):
    context = {
        'page': forms.section1.forms[0],
    }
    return render(request, 'register_business/form.html', context)
