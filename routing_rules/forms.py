from django.urls import reverse_lazy

from cases.services import get_case_types, get_flags_for_team_of_level
from core.services import get_statuses, get_countries
from lite_forms.components import (
    FormGroup,
    Form,
    Select,
    AutocompleteInput,
    TextInput,
    Checkboxes,
    Option,
    RadioButtons,
    BackLink,
    HiddenField,
)
from lite_forms.generators import confirm_form
from lite_forms.helpers import conditional
from teams.services import get_users_team_queues, get_users_by_team
from users.services import get_gov_user

additional_rules = [
    Option("case_types", "Case Types"),
    Option("flags", "Flags"),
    Option("country", "Country"),
    Option("users", "Users"),
]


def initial_routing_rule_questions(request, is_editing: bool):
    if is_editing:
        title = "Edit the routing rule"
    else:
        title = "Create a new routing rule"

    return Form(
        title=title,
        questions=[
            Select(title="Select a case status", name="status", options=get_statuses(request, True)),
            AutocompleteInput(
                title="Select a team work queue",
                name="queue",
                options=get_users_team_queues(request, request.user.lite_api_user_id, True),
            ),
            TextInput(title="Enter a tier number", name="tier"),
            HiddenField(name="additional_rules[]", value=None),
            Checkboxes(
                title="Select the combination of options you need to create the case routing rule",
                name="additional_rules[]",
                options=additional_rules,
            ),
        ],
        back_link=BackLink("Back to routing rules", reverse_lazy("routing_rules:list")),
    )


def select_case_type(request):
    return Form(
        title="Select case types",
        questions=[
            Checkboxes(
                name="case_types[]",
                options=[
                    Option(option["id"], option["reference"]["value"]) for option in get_case_types(request, False)
                ],
            )
        ],
    )


def select_flags(request, team_id):
    return Form(
        title="Select flags",
        questions=[
            Checkboxes(
                name="flags[]",
                options=[
                    Option(flag["id"], flag["name"])
                    for flag in get_flags_for_team_of_level(
                        request, level="", team_id=team_id, include_system_flags=True
                    )[0]
                ],
            )
        ],
    )


def select_country(request):
    return Form(
        title="Select a country",
        questions=[AutocompleteInput(name="country", options=get_countries(request, convert_to_options=True),)],
    )


def select_team_member(request, team_id):
    return Form(
        title="Select a team member to assign the case to",
        questions=[
            RadioButtons(
                name="user",
                options=[Option(user["id"], user["email"]) for user in get_users_by_team(request, team_id)[0]["users"]],
            )
        ],
    )


def routing_rule_form_group(request, additional_rules, is_editing=False):
    team_id = get_gov_user(request)[0]["user"]["team"]["id"]
    return FormGroup(
        [
            initial_routing_rule_questions(request, is_editing),
            conditional("case_types" in additional_rules, select_case_type(request)),
            conditional("flags" in additional_rules, select_flags(request, team_id)),
            conditional("country" in additional_rules, select_country(request)),
            conditional("users" in additional_rules, select_team_member(request, team_id)),
        ]
    )


def deactivate_or_activate_routing_rule_form(title, description, confirm_text, status):
    return confirm_form(
        title=title,
        description=description,
        back_link_text="Back to routing rules list",
        back_url=reverse_lazy("routing_rules:list"),
        yes_label=confirm_text,
        no_label="Cancel",
        hidden_field=status,
        confirmation_name="confirm",
    )
