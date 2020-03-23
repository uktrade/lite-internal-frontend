from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from conf.constants import Permission
from core.helpers import convert_dict_to_query_params
from core.objects import Tab
from core.services import get_user_permissions
from lite_content.lite_internal_frontend import strings
from lite_content.lite_internal_frontend.organisations import OrganisationsPage
from lite_forms.components import FiltersBar, TextInput, Select, Option
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form
from lite_forms.views import MultiFormView
from organisations.forms import register_business_forms, register_hmrc_organisation_forms, edit_business_forms
from organisations.services import (
    get_organisations,
    get_organisation_sites,
    get_organisation,
    post_organisations,
    put_organisation,
    validate_post_organisation,
    get_organisation_members)


class OrganisationList(TemplateView):
    """
    Show all organisations.
    """

    def get(self, request, **kwargs):
        search_term = request.GET.get("search_term", "").strip()
        org_type = request.GET.get("org_type", "").strip()

        params = {"page": int(request.GET.get("page", 1))}
        if search_term:
            params["search_term"] = search_term
        if org_type:
            params["org_type"] = org_type

        organisations, _ = get_organisations(request, convert_dict_to_query_params(params))

        filters = FiltersBar(
            [
                TextInput(name="search_term", title=OrganisationsPage.Filters.NAME),
                Select(
                    name="org_type",
                    title=OrganisationsPage.Filters.TYPE,
                    options=[
                        Option("individual", OrganisationsPage.Filters.Types.INDIVIDUAL),
                        Option("commercial", OrganisationsPage.Filters.Types.COMMERCIAL),
                        Option("hmrc", OrganisationsPage.Filters.Types.HMRC),
                    ],
                ),
            ]
        )

        context = {
            "data": organisations,
            "page": params.pop("page"),
            "params_str": convert_dict_to_query_params(params),
            "filters": filters,
            "search_term": params.get("search_term", ""),
            "can_manage_organisations": Permission.MANAGE_ORGANISATIONS.value in get_user_permissions(request),
        }
        return render(request, "organisations/index.html", context)


class OrganisationView(TemplateView):
    organisation_id = None
    organisation = None
    additional_context = {}

    def get_additional_context(self):
        return self.additional_context

    def get(self, request, **kwargs):
        self.organisation_id = kwargs["pk"]
        self.organisation = get_organisation(request, self.organisation_id)

        context = {
            "organisation": self.organisation,
            "tabs": [
                Tab("details", "Details", reverse_lazy("organisations:organisation", kwargs={"pk": self.organisation_id})),
                Tab("members", "Members", reverse_lazy("organisations:organisation_members", kwargs={"pk": self.organisation_id})),
                Tab("sites", "Sites", reverse_lazy("organisations:organisation_sites", kwargs={"pk": self.organisation_id})),
            ],
        }
        context.update(self.get_additional_context())
        return render(request, f"organisations/organisation/{self.template_name}.html", context)


class OrganisationDetails(OrganisationView):
    template_name = "details"


class OrganisationMembers(OrganisationView):
    template_name = "members"

    def get_additional_context(self):
        return {"members": get_organisation_members(self.request, self.organisation_id)}


class OrganisationSites(OrganisationView):
    template_name = "sites"

    def get_additional_context(self):
        return {"sites": get_organisation_sites(self.request, self.organisation_id)}


class RegisterBusiness(TemplateView):
    forms = None

    def dispatch(self, request, *args, **kwargs):
        individual = request.POST.get("type") == "individual"
        name = request.POST.get("name")
        self.forms = register_business_forms(individual, name) if name else register_business_forms(individual)

        return super(RegisterBusiness, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0])

    def post(self, request, **kwargs):
        response, _ = submit_paged_form(request, self.forms, post_organisations)

        if response:
            return response

        messages.success(request, strings.ORGANISATION_CREATION_SUCCESS)
        return redirect("organisations:organisations")


class RegisterHMRC(TemplateView):
    forms = None

    def dispatch(self, request, *args, **kwargs):
        name = request.POST.get("name")
        self.forms = register_hmrc_organisation_forms(name) if name else register_hmrc_organisation_forms()

        return super(RegisterHMRC, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0])

    def post(self, request, **kwargs):
        response, _ = submit_paged_form(request, self.forms, post_organisations)

        if response:
            return response

        messages.success(request, strings.HMRC_ORGANISATION_CREATION_SUCCESS)
        return redirect("organisations:hmrc")


class EditOrganisation(MultiFormView):
    forms = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate_action = validate_post_organisation
        self.post_action = put_organisation

    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        organisation = get_organisation(request, str(self.object_pk))
        self.data = organisation
        individual = request.POST.get("type") == "individual"
        self.forms = edit_business_forms(request, individual)
        self.success_url = reverse_lazy("organisations:organisations")

    def on_submission(self, request, **kwargs):
        if int(self.request.POST.get("form_pk")) == len(self.forms.forms) - 1:
            self.action = self.post_action
        else:
            self.action = self.validate_action
