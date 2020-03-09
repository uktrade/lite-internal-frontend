from cases.services import get_case_types
from core.services import get_control_list_entries, get_countries
from flags.services import _get_team_flags, get_goods_flags, get_destination_flags, get_cases_flags
from lite_content.lite_internal_frontend import strings
from django.urls import reverse_lazy
from lite_forms.components import TextInput, Select, Option, BackLink, Form, FormGroup, RadioButtons, AutocompleteInput

_name = TextInput(title="Name", name="name")

_level = Select(
    name="level",
    options=[
        Option("Case", "Case"),
        Option("Organisation", "Organisation"),
        Option("Destination", "Destination"),
        Option("Good", "Good"),
    ],
    title="Level",
)

_back_link = BackLink("Back to Flags", reverse_lazy("flags:flags"))


def add_flag_form():
    return Form(
        title=strings.Flags.CREATE, questions=[_name, _level,], back_link=_back_link, default_button_name="Create"
    )


def edit_flag_form():
    return Form(title="Edit Flag", questions=[_name,], back_link=_back_link)


def select_flagging_rule_type():
    return Form(
        title="flagging rule type",
        questions=[
            RadioButtons(
                title="",
                name="type",
                options=[
                    Option(key="good", value="Good"),
                    Option(key="destination", value="Destination"),
                    Option(key="application", value="Application"),
                ],
            )
        ],
    )


def select_condition_and_flag(request, type: str):
    if type == "good":
        condition = AutocompleteInput(
            title="good condition", name="condition", options=get_control_list_entries(request, convert_to_options=True)
        )
        flags = get_goods_flags(request=request, convert_to_options=True)
    elif type == "destination":
        condition = Select(
            title="destination condition", name="condition", options=get_countries(request, convert_to_options=True)
        )
        flags = get_destination_flags(request=request, convert_to_options=True)
    elif type == "application":
        case_type_options = [Option(option["key"], option["value"]) for option in get_case_types(request)]
        condition = Select(title="Application Type", name="condition", options=case_type_options)
        flags = get_cases_flags(request=request, convert_to_options=True)
    else:
        condition = []
        flags = []
    return Form(
        title="Flagging rule condition and flag",
        questions=[condition, Select(title="Flag", name="flag", options=flags),],
    )


def create_flagging_rules_formGroup(request=None, type=None):
    return FormGroup([select_flagging_rule_type(), select_condition_and_flag(request=request, type=type)],)
