from django.urls import reverse_lazy

from cases.services import get_case_types, get_flags_for_team_of_level
from core.services import get_statuses, get_countries
from lite_content.lite_internal_frontend.routing_rules import (
    AdditionalRules,
    DeactivateForm,
    ActivateForm,
    Forms,
)
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
from teams.services import get_users_by_team, get_teams, get_team_queues

additional_rules = [
    Option("case_types", AdditionalRules.CASE_TYPES),
    Option("flags", AdditionalRules.FLAGS),
    Option("country", AdditionalRules.COUNTRY),
    Option("users", AdditionalRules.USERS),
]


def select_a_team(request):
    return Form(
        title=Forms.TEAM,
        questions=[RadioButtons(name="team", options=get_teams(request, True))],
        back_link=BackLink(Forms.BACK_BUTTON, reverse_lazy("routing_rules:list")),
    )


def initial_routing_rule_questions(request, team_id, is_editing: bool):
    if is_editing:
        title = Forms.EDIT_TITLE
    else:
        title = Forms.CREATE_TITLE

    return Form(
        title=title,
        questions=[
            Select(title=Forms.CASE_STATUS, name="status", options=get_statuses(request, True)),
            AutocompleteInput(title=Forms.QUEUE, name="queue", options=get_team_queues(request, team_id, True, True),),
            TextInput(title=Forms.TIER, name="tier"),
            HiddenField(name="additional_rules[]", value=None),
            Checkboxes(title=Forms.ADDITIONAL_RULES, name="additional_rules[]", options=additional_rules,),
        ],
        back_link=BackLink(Forms.BACK_BUTTON, reverse_lazy("routing_rules:list")),
    )


def select_case_type(request):
    return Form(
        title=Forms.CASE_TYPES,
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
        title=Forms.FLAGS,
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
        title=Forms.COUNTRY,
        questions=[AutocompleteInput(name="country", options=get_countries(request, convert_to_options=True),)],
    )


def select_team_member(request, team_id):
    return Form(
        title=Forms.USER,
        questions=[RadioButtons(name="user", options=get_users_by_team(request, team_id, convert_to_options=True),)],
    )


def routing_rule_form_group(request, additional_rules, team_id, is_editing=False, select_team=False):
    return FormGroup(
        [
            conditional(select_team, select_a_team(request),),
            initial_routing_rule_questions(request, team_id, is_editing),
            conditional("case_types" in additional_rules, select_case_type(request)),
            conditional("flags" in additional_rules, select_flags(request, team_id)),
            conditional("country" in additional_rules, select_country(request)),
            conditional("users" in additional_rules, select_team_member(request, team_id)),
        ]
    )


def deactivate_or_activate_routing_rule_form(activate, status):
    if activate:
        title = ActivateForm.TITLE
        description = ActivateForm.DESCRIPTION
        yes_label = ActivateForm.YES_LABEL
        no_label = ActivateForm.NO_LABEL
    else:
        title = DeactivateForm.TITLE
        description = DeactivateForm.DESCRIPTION
        yes_label = DeactivateForm.YES_LABEL
        no_label = DeactivateForm.NO_LABEL

    return confirm_form(
        title=title,
        description=description,
        back_link_text=Forms.BACK_BUTTON,
        back_url=reverse_lazy("routing_rules:list"),
        yes_label=yes_label,
        no_label=no_label,
        hidden_field=status,
        confirmation_name="confirm",
    )
