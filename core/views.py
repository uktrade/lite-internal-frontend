from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import RedirectView


class Index(RedirectView):
    url = reverse_lazy("queues:cases")


def menu(request):
    return render(request, "core/menu.html", {"title": "Menu"})
