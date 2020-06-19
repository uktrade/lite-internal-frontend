import json

from django.conf import settings
from django.views.generic import FormView, TemplateView

from spire import forms, helpers


class SpireLicenseSearch(FormView):
    form_class = forms.SpireLicenseSearchForm
    template_name = "spire/licence-search.html"

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
        response = helpers.spire_client.list_licences(
            organisation=settings.LITE_SPIRE_ARCHIVE_EXAMPLE_ORGANISATION_ID, **filters
        )
        response.raise_for_status()
        parsed = response.json()
        context["results"] = parsed["results"]
        # the {% paginator %} in the template needs this shaped data exposed
        context["data"] = {"total_pages": parsed["count"] // form.page_size}
        return context


class SpireLicenceDetail(TemplateView):
    template_name = "spire/licence.html"

    def get_context_data(self, **kwargs):
        response = helpers.spire_client.get_licence(self.kwargs["id"])
        response.raise_for_status()
        return super().get_context_data(licence=response.json(),**kwargs)
