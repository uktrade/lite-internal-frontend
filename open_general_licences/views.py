from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from core.services import get_countries, get_control_list_entries
from lite_forms.components import FiltersBar, Select, TextInput, AutocompleteInput
from lite_forms.generators import confirm_form
from lite_forms.views import SummaryListFormView, SingleFormView
from open_general_licences.enums import OpenGeneralExportLicences
from open_general_licences.forms import new_open_general_licence_forms
from open_general_licences.services import (
    get_open_general_licences,
    post_open_general_licences,
    get_open_general_licence, patch_open_general_licence,
)


class ListView(TemplateView):
    def get(self, request, *args, **kwargs):
        open_general_licences = get_open_general_licences(request, **request.GET)
        control_list_entries = get_control_list_entries(request, True)
        countries = get_countries(request, True)

        filters = FiltersBar(
            [
                TextInput(name="name", title="name"),
                Select(name="case_type", title="type", options=OpenGeneralExportLicences.as_options()),
                AutocompleteInput(name="control_list_entry", title="control list entry", options=control_list_entries),
                AutocompleteInput(name="country", title="country", options=countries),
            ]
        )

        context = {
            "filters": filters,
            "tab": request.GET.get("status", "active"),
            "open_general_licences": open_general_licences,
        }
        return render(request, "open-general-licences/index.html", context)


class DetailView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {"open_general_licence": get_open_general_licence(request, kwargs["pk"])}
        return render(request, "open-general-licences/open-general-licence.html", context)


class CreateView(SummaryListFormView):
    def init(self, request, **kwargs):
        self.forms = new_open_general_licence_forms(request)
        self.action = post_open_general_licences
        self.summary_list_title = "Confirm details about this licence"
        self.summary_list_button = "Submit"
        self.summary_list_notice_title = None
        self.summary_list_notice_text = None
        self.hide_titles = True
        self.success_message = "OGL added successfully"
        self.success_url = reverse("open_general_licences:open_general_licences")


class UpdateView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "open_general_licences/index.html", {})


class ChangeStatusView(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.object = get_open_general_licence(request, self.object_pk)
        self.action = patch_open_general_licence
        self.success_message = "OGL de/re activated successfully"
        self.success_url = reverse("open_general_licences:open_general_licence", kwargs={"pk": self.object_pk})

    def get_form(self):
        title = "Are you sure you want to deactivate OGL (" + self.object["name"] + ")"
        # title = "Are you sure you want to reactivate OGL (" + self.object["name"] + ")"

        return confirm_form(
            title=title,
            description="This will prevent exporters from using this licence. You can change this in the future.",
            back_link_text="Back",
            back_url="swag",
            yes_label="Yes",
            no_label="No",
            side_by_side=True,
            confirmation_name="confirm",
        )
