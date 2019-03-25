from django.shortcuts import render


def show_orgs(request):
    context = {
        'title': 'List of Registered Organizations',
    }
    return render(request, 'new_application/index.html', context)

