from django.template.defaultfilters import default
from django.urls import reverse_lazy

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
    Summary,
)
from lite_forms.styles import HeadingStyle

from core.services import get_control_list_entries, get_gov_pv_gradings
from picklists.services import get_picklists_for_input


def respond_to_clc_query_form(request, queue_pk, case):
    return Form(
        title=cases.RespondClCQueryForm.TITLE,
        questions=[
            Summary(
                values={
                    cases.RespondClCQueryForm.Summary.DESCRIPTION: case["query"]["good"]["description"],
                    cases.RespondClCQueryForm.Summary.CONTROL_LIST_ENTRIES: default(
                        case["query"]["good"].get("control_list_entries"),
                        cases.RespondClCQueryForm.Summary.NO_CONTROL_LIST_ENTRY,
                    ),
                },
                classes=["app-inset-text"],
            ),
            RadioButtons(
                title=cases.RespondClCQueryForm.Controlled.TITLE,
                name="is_good_controlled",
                options=[
                    Option(
                        key="yes",
                        value=cases.RespondClCQueryForm.Controlled.YES,
                        components=[
                            control_list_entries_question(
                                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                                title=cases.RespondClCQueryForm.CONTROL_LIST_ENTRY,
                            ),
                        ],
                    ),
                    Option(key="no", value=cases.RespondClCQueryForm.Controlled.NO),
                ],
            ),
            RadioButtons(
                title=cases.RespondClCQueryForm.ReportSummary.TITLE,
                name="report_summary",
                options=get_picklists_for_input(request, "report_summary", convert_to_options=True, include_none=True),
                description=cases.RespondClCQueryForm.ReportSummary.DESCRIPTION,
            ),
            TextArea(
                title=cases.RespondClCQueryForm.COMMENT, name="comment", optional=True, extras={"max_length": 500,}
            ),
            HiddenField("validate_only", True),
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
        questions=[
            Heading(case["reference_code"], HeadingStyle.S),
            Summary(values={"Description": case["query"]["good"]["description"]}, classes=["app-inset-text"],),
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
            TextArea(
                title=cases.RespondGradingQueryForm.COMMENT, name="comment", optional=True, extras={"max_length": 500,}
            ),
            HiddenField("validate_only", True),
        ],
        default_button_name=cases.RespondGradingQueryForm.BUTTON,
        back_link=BackLink(
            cases.RespondGradingQueryForm.BACK,
            reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": case["id"]}),
        ),
    )
