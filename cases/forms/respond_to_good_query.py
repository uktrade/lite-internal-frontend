from django.template.defaultfilters import default
from django.urls import reverse_lazy

from core.builtins.custom_tags import default_na
from lite_content.lite_internal_frontend import cases
from lite_forms.common import control_list_entries_question
from lite_forms.components import (
    Form,
    BackLink,
    RadioButtons,
    Option,
    TextArea,
    Heading,
    HiddenField,
    Group,
    TextInput,
    Select,
    Summary, DetailComponent, Label,
)
from lite_forms.styles import HeadingStyle

from core.services import get_control_list_entries, get_gov_pv_gradings
from picklists.services import get_picklists_for_input


def respond_to_clc_query_form(request, queue_pk, case):
    return Form(
        title="Respond to query",
        description="You won't be able to change this once you've submitted.",
        questions=[
                Heading("Query", HeadingStyle.S),
                Summary(
                    values={
                        "Description of good": case["query"]["good"]["description"],
                        "Part number": default_na(case["query"]["good"]["part_number"]),
                        "Is this good controlled?": case["query"]["good"]["is_good_controlled"]["value"],
                        "What do you think the control list entry is?": case["query"]["clc_control_list_entry"],
                        "Why do you think this?": case["query"]["clc_raised_reasons"]
                    },
                    classes=["govuk-inset-text", "govuk-summary-list--no-border", "govuk-!-padding-top-0",
                             "govuk-!-padding-bottom-0", "govuk-!-padding-left-6"]
                ),

                Heading("Your response", HeadingStyle.S),
                RadioButtons(
                    title=cases.RespondClCQueryForm.Controlled.TITLE,
                    name="is_good_controlled",
                    classes=["govuk-radios--small"],
                    options=[
                        Option(
                            key="yes",
                            value=cases.RespondClCQueryForm.Controlled.YES,
                            components=[
                                control_list_entries_question(
                                    control_list_entries=get_control_list_entries(None,
                                                                                  convert_to_options=True),
                                    title=cases.RespondClCQueryForm.CONTROL_LIST_ENTRY,
                                ),
                                RadioButtons(
                                    title=cases.RespondClCQueryForm.ReportSummary.TITLE,
                                    name="report_summary",
                                    options=get_picklists_for_input(request, "report_summary",
                                                                    convert_to_options=True),
                                ),
                            ],
                        ),
                        Option(key="no", value=cases.RespondClCQueryForm.Controlled.NO),
                    ],
                ),
                DetailComponent(title="Explain why you're making this decision (optional)",
                                components=[
                                    TextArea(
                                        name="comment",
                                        extras={"max_length": 500, }
                                    ),
                                ]),
        ],
        default_button_name=cases.RespondClCQueryForm.BUTTON,
        back_link=BackLink(
            cases.RespondClCQueryForm.BACK, reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": case["id"]}),
        ),
        container="case"
    )


def respond_to_grading_query_form(queue_pk, case):
    pv_gradings = get_gov_pv_gradings(request=None, convert_to_options=True)
    return Form(
        title=cases.RespondGradingQueryForm.TITLE,
        description="You won't be able to change this once you've submitted",
        questions=[
            Heading("Query", HeadingStyle.S),
            Summary(
                values={
                    "Description of good": case["query"]["good"]["description"],
                    "Part number": default_na(case["query"]["good"]["part_number"]),
                    "Is this good controlled?": case["query"]["good"]["is_good_controlled"]["value"],
                    "What do you think the control list entry is?": case["query"]["clc_control_list_entry"],
                    "Why do you think this?": case["query"]["clc_raised_reasons"]
                },
                classes=["govuk-inset-text", "govuk-summary-list--no-border", "govuk-!-padding-top-0",
                         "govuk-!-padding-bottom-0", "govuk-!-padding-left-6"]
            ),
            Heading("Your response", HeadingStyle.S),
            Group(
                components=[
                    TextInput(title=cases.RespondGradingQueryForm.Grading.PREFIX, name="prefix", optional=True),
                    Select(
                        # request not supplied since static endpoints don't require it.
                        options=pv_gradings,
                        title=cases.RespondGradingQueryForm.Grading.GRADING,
                        name="grading",
                    ),
                    TextInput(title=cases.RespondGradingQueryForm.Grading.SUFFIX, name="suffix", optional=True),
                ],
                classes=["app-pv-grading-inputs"],
            ),
            DetailComponent(title="Explain why you're making this decision (optional)",
                            components=[
                                TextArea(
                                    name="comment",
                                    extras={"max_length": 500, }
                                ),
                            ]),
        ],
        default_button_name=cases.RespondGradingQueryForm.BUTTON,
        back_link=BackLink(
            cases.RespondGradingQueryForm.BACK,
            reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": case["id"]}),
        ),
        container="case"
    )
