from cases.services import get_case_types
from core.services import get_countries
from flags.services import get_goods_flags, get_destination_flags, get_cases_flags
from lite_content.lite_internal_frontend import strings
from django.urls import reverse_lazy

from lite_content.lite_internal_frontend.flags import CreateFlagForm, EditFlagForm
from lite_forms.components import (
    TextInput,
    Select,
    Option,
    BackLink,
    Form,
    FormGroup,
    RadioButtons,
    AutocompleteInput,
    NumberInput,
)
from lite_forms.generators import confirm_form

options = [
    Option("Case", "Case"),
    Option("Organisation", "Organisation"),
    Option("Destination", "Destination"),
    Option("Good", "Good"),
]


_levels = [
    Option(key="Good", value=strings.FlaggingRules.Create.Type.GOOD),
    Option(key="Destination", value=strings.FlaggingRules.Create.Type.DESTINATION),
    Option(key="Case", value=strings.FlaggingRules.Create.Type.APPLICATION),
]


def add_flag_form():
    return Form(
        title=CreateFlagForm.TITLE,
        description=CreateFlagForm.DESCRIPTION,
        questions=[
            TextInput(title=CreateFlagForm.Name.TITLE, description=CreateFlagForm.Name.DESCRIPTION, name="name"),
            Select(
                title=CreateFlagForm.Level.TITLE,
                description=CreateFlagForm.Level.DESCRIPTION,
                name="level",
                options=options,
            ),
            RadioButtons(
                title="Colour",
                description="You can help convey information through use of colour",
                name="colour",
                classes=["app-radios--flag-colours"],
                options=[
                    Option("default", "Default"),
                    Option("red", "Red", classes=["app-radios__item--red"]),
                    Option("yellow", "Yellow", classes=["app-radios__item--yellow"]),
                    Option("green", "Green", classes=["app-radios__item--green"]),
                    Option("blue", "Blue", classes=["app-radios__item--blue"]),
                    Option("purple", "Purple", classes=["app-radios__item--purple"]),
                    Option("orange", "Orange", classes=["app-radios__item--orange"]),
                    Option("brown", "Brown", classes=["app-radios__item--brown"]),
                    Option("turquoise", "Turquoise", classes=["app-radios__item--turquoise"]),
                    Option("pink", "Pink", classes=["app-radios__item--pink"]),
                ],
            ),
            TextInput(
                name="label",
                title="Colour meaning",
                description="We'll show this value when you hover over the flag to provide more information",
            ),
            NumberInput(name="priority", title="Priority", description="This relates to ordering"),
        ],
        default_button_name=CreateFlagForm.SUBMIT_BUTTON,
        back_link=BackLink(CreateFlagForm.BACK_LINK, reverse_lazy("flags:flags")),
        javascript_imports=["/assets/javascripts/add-edit-flags.js"],
    )


def edit_flag_form():
    return Form(
        title=EditFlagForm.TITLE,
        questions=[
            TextInput(title=EditFlagForm.Name.TITLE, description=EditFlagForm.Name.DESCRIPTION, name="name"),
            RadioButtons(
                title="Colour",
                name="colour",
                classes=["app-radios--flag-colours"],
                options=[
                    Option("default", "Default"),
                    Option("red", "Red", classes=["app-radios__item--red"]),
                    Option("yellow", "Yellow", classes=["app-radios__item--yellow"]),
                    Option("green", "Green", classes=["app-radios__item--green"]),
                    Option("blue", "Blue", classes=["app-radios__item--blue"]),
                    Option("purple", "Purple", classes=["app-radios__item--purple"]),
                    Option("orange", "Orange", classes=["app-radios__item--orange"]),
                    Option("brown", "Brown", classes=["app-radios__item--brown"]),
                    Option("turquoise", "Turquoise", classes=["app-radios__item--turquoise"]),
                    Option("pink", "Pink", classes=["app-radios__item--pink"]),
                ],
            ),
            TextInput(name="label", title="Label"),
            NumberInput(name="priority", title="Priority"),
        ],
        back_link=BackLink(EditFlagForm.BACK_LINK, reverse_lazy("flags:flags")),
        default_button_name=EditFlagForm.SUBMIT_BUTTON,
        javascript_imports=["/assets/javascripts/add-edit-flags.js"],
    )


def select_flagging_rule_type():
    return Form(
        title=strings.FlaggingRules.Create.Type.TITLE,
        questions=[RadioButtons(name="level", options=_levels,)],
        back_link=BackLink(strings.FlaggingRules.Create.BACKLINK, reverse_lazy("flags:flagging_rules")),
        default_button_name=strings.FlaggingRules.Create.Type.SAVE,
    )


def select_condition_and_flag(request, type: str):
    title = ""
    condition = []
    flags = []
    if type == "Good":
        title = strings.FlaggingRules.Create.Condition_and_flag.GOOD_TITLE
        condition = TextInput(title=strings.FlaggingRules.Create.Condition_and_flag.GOOD, name="matching_value",)
        flags = get_goods_flags(request=request, convert_to_options=True)
    elif type == "Destination":
        title = strings.FlaggingRules.Create.Condition_and_flag.DESTINATION_TITLE
        condition = AutocompleteInput(
            title=strings.FlaggingRules.Create.Condition_and_flag.DESTINATION,
            name="matching_value",
            options=get_countries(request, convert_to_options=True),
        )
        flags = get_destination_flags(request=request, convert_to_options=True)
    elif type == "Case":
        title = strings.FlaggingRules.Create.Condition_and_flag.APPLICATION_TITLE
        case_type_options = [Option(option["key"], option["value"]) for option in get_case_types(request)]
        condition = Select(
            title=strings.FlaggingRules.Create.Condition_and_flag.APPLICATION,
            name="matching_value",
            options=case_type_options,
        )
        flags = get_cases_flags(request=request, convert_to_options=True)

    return Form(
        title=title,
        questions=[
            condition,
            Select(title=strings.FlaggingRules.Create.Condition_and_flag.FLAG, name="flag", options=flags),
        ],
    )


def create_flagging_rules_formGroup(request=None, type=None):
    return FormGroup([select_flagging_rule_type(), select_condition_and_flag(request=request, type=type)],)


def deactivate_or_activate_flagging_rule_form(title, description, confirm_text, status):
    return confirm_form(
        title=title,
        description=description,
        back_link_text=strings.FlaggingRules.Status.BACK,
        back_url=reverse_lazy("flags:flagging_rules"),
        yes_label=confirm_text,
        no_label=strings.FlaggingRules.Status.CANCEL,
        hidden_field=status,
        confirmation_name="confirm",
    )
