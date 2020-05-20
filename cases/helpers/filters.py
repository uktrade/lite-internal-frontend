from core.services import get_control_list_entries, get_countries
from flags.services import get_flags
from lite_content.lite_internal_frontend.cases import CasesListPage
from lite_forms.components import (
    FiltersBar, Option, AutocompleteInput, Checkboxes, Select, DateInput, TextInput, TokenBar
)
from lite_forms.helpers import conditional


def case_filters_bar(request, case_data) -> FiltersBar:
    """
    Returns a FiltersBar for the case search page.
    """
    filters = case_data["results"]["filters"]
    statuses = [Option(option["key"], option["value"]) for option in filters["statuses"]]
    case_types = [Option(option["key"], option["value"]) for option in filters["case_types"]]
    gov_users = [Option(option["id"], option["full_name"]) for option in filters["gov_users"]]
    advice_types = [Option(option["key"], option["value"]) for option in filters["advice_types"]]
    sla_days = [Option(i, i) for i in range(99)]

    return FiltersBar(
        [
            TextInput(name="case_reference", title="case reference"),
            Select(name="case_type", title=CasesListPage.Filters.CASE_TYPE, options=case_types),
            Select(name="status", title=CasesListPage.Filters.CASE_STATUS, options=statuses),
            AutocompleteInput(
                name="case_officer",
                title=CasesListPage.Filters.CASE_OFFICER,
                options=[Option("not_assigned", CasesListPage.Filters.NOT_ASSIGNED), *gov_users],
            ),
            AutocompleteInput(
                name="assigned_user",
                title=CasesListPage.Filters.ASSIGNED_USER,
                options=[Option("not_assigned", CasesListPage.Filters.NOT_ASSIGNED), *gov_users],
            ),
            conditional(
                case_data["results"]["is_work_queue"],
                Checkboxes(
                    name="hidden",
                    options=[Option("true", CasesListPage.Filters.HIDDEN)],
                    classes=["govuk-checkboxes--small"],
                ),
            ),
        ],
        advanced_filters=[
            TextInput(name="exporter_application_reference", title="exporter application reference"),
            TextInput(name="exporter_site_name", title="exporter site name"),
            TextInput(name="exporter_site_address", title="exporter site address"),
            Select(name="final_advice_type", title="final advice type", options=advice_types),
            Select(name="team_advice_type", title="team advice type", options=advice_types),
            Select(name="max_sla_days_remaining", title="max SLA days remaining", options=sla_days),
            Select(name="min_sla_days_remaining", title="min SLA days remaining", options=sla_days),
            Select(name="sla_days_elapsed", title="SLA days elapsed", options=sla_days),
            DateInput(name="submitted_from", title="submitted from", prefix="submitted_from_", inline_title=True),
            DateInput(name="submitted_to", title="submitted to", prefix="submitted_to_", inline_title=True),
            DateInput(name="finalised_from", title="finalised from", prefix="finalised_from_", inline_title=True),
            DateInput(name="finalised_to", title="finalised to", prefix="finalised_to_", inline_title=True),
            TextInput(name="party_name", title="party name"),
            TextInput(name="party_address", title="party address"),
            TextInput(name="goods_related_description", title="goods related description"),
            AutocompleteInput(name="country", title="country", options=get_countries(request, convert_to_options=True)),
            AutocompleteInput(
                name="control_list_entry",
                title="control list entry",
                options=get_control_list_entries(request, convert_to_options=True),
            ),
            TokenBar(name="flags", title="flags", options=[
                Option(flag["id"], flag["name"])
                for flag in get_flags(request, disable_pagination=True)
            ]),
            Checkboxes(
                name="sort_by_sla_remaining",
                options=[Option("true", "Sort by SLA remaining")],
                classes=["govuk-checkboxes--small"],
            )
        ],
    )
