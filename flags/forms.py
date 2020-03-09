from flags.services import _get_team_flags
from lite_content.lite_internal_frontend import strings
from django.urls import reverse_lazy
from lite_forms.components import TextInput, Select, Option, BackLink, Form, FormGroup, RadioButtons

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
                    Option(key="Good", value="good"),
                    Option(key="Destination", value="destination"),
                    Option(key="Application", value="application"),
                ],
            )
        ],
    )


def select_condtion_and_flag(type: str):
    return Form(
        title="Flagging rule condition and flag",
        questions=[Select(title="", name="condition", options=[],), Select(title="Flag", name="flag", options=[])],
    )


def create_flagging_rules_formGroup():
    return FormGroup([select_flagging_rule_type(), select_condtion_and_flag(type="")],)
