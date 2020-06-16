from django.conf import settings
from django.shortcuts import render
from django.views.generic import FormView

from core import forms, helpers


def menu(request):
    return render(request, "core/menu.html", {"title": "Menu"})


class SpireLicenseSearch(FormView):
    form_class = forms.SpireLicenseSearchForm
    template_name = "core/historic-spire-license-search.html"

    def get_form_kwargs(self):
        # allows form to be submitted on GET by making self.get_form() return bound form
        kwargs = super().get_form_kwargs()
        if self.request.GET:
            kwargs["data"] = self.request.GET
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        filters = form.cleaned_data if form.is_valid() else {}
        respoonse = helpers.spire_client.list_licenses(
            organisation=settings.LITE_SPIRE_ARCHIVE_EXAMPLE_ORGANISATION_ID, **filters
        )
        respoonse.raise_for_status()
        parsed = respoonse.json()
        context["results"] = parsed["results"]
        # the {% paginator %} in the template needs this shaped data exposed
        context["data"] = {"total_pages": parsed["count"] // form.page_size}
        return context
