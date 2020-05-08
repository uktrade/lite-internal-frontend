from django.urls import reverse

from cases.constants import CaseType
from cases.objects import Case
from core.components import PicklistPicker
from core.services import get_gov_pv_gradings, get_pv_gradings
from lite_content.lite_internal_frontend.strings import cases
from lite_forms.components import (
    Form,
    RadioButtons,
    Option,
    BackLink,
    TextArea,
    Checkboxes,
    HelpSection,
    HTMLBlock,
    Group,
    TextInput,
    Custom, Select,
)
from lite_forms.helpers import conditional
from picklists.services import get_picklists_for_input


def give_advice_form(request, case: Case, tab, queue_pk, denial_reasons, show_warning=False):
    return Form(
        title=cases.AdviceRecommendationForm.TITLE,
        questions=[
            conditional(
                show_warning,
                HTMLBlock(
                    "<div class='govuk-warning-text'>"
                    + "<span class='govuk-warning-text__icon' aria-hidden='true'>!</span>"
                    + "<strong class='govuk-warning-text__text'>"
                    + "<span class='govuk-warning-text__assistive'>Warning</span>"
                    + "The advice for your selected items does not match. However, you can still override the advice."
                    + "</strong>"
                    + "</div>"
                ),
            ),
            RadioButtons(
                name="type",
                options=[
                    Option(key="approve", value=cases.AdviceRecommendationForm.RadioButtons.GRANT, components=[
                        conditional(CaseType.is_mod(case["case_type"]["sub_type"]["key"]),
                                    Select(name="pv_grading_approve", title="Select a grading",
                                           options=get_pv_gradings(request=None, convert_to_options=True)))
                    ]),
                    Option(
                        key="proviso",
                        value=cases.AdviceRecommendationForm.RadioButtons.PROVISO,
                        components=[
                            conditional(CaseType.is_mod(case["case_type"]["sub_type"]["key"]),
                                        Select(name="pv_grading_proviso", title="Select a grading",
                                               options=get_pv_gradings(request=None, convert_to_options=True))),
                            TextArea(
                                title="Proviso",
                                description="This will appear on the generated documentation",
                                extras={"max_length": 5000},
                                name="proviso",
                            ),
                            PicklistPicker(target="proviso", items=get_picklists_for_input(request, "proviso")),
                        ],
                    ),
                    Option(
                        key="refuse",
                        value=conditional(
                            case.sub_type == CaseType.OPEN.value,
                            cases.AdviceRecommendationForm.RadioButtons.REJECT,
                            cases.AdviceRecommendationForm.RadioButtons.REFUSE,
                        ),
                        components=[
                            Group(
                                [
                                    Checkboxes(
                                        title=conditional(
                                            key == "1", "Select the appropriate denial reasons for your selection"
                                        ),
                                        name="denial_reasons[]",
                                        options=denial_reasons[key],
                                        classes=["govuk-checkboxes--small", "govuk-checkboxes--inline"],
                                    )
                                    for key in denial_reasons.keys()
                                ],
                                ["app-advice__checkboxes"],
                            )
                        ],
                    ),
                    Option(key="no_licence_required", value=cases.AdviceRecommendationForm.RadioButtons.NLR),
                    Option(
                        key="not_applicable",
                        value=cases.AdviceRecommendationForm.RadioButtons.NOT_APPLICABLE,
                        show_or=True,
                    ),
                ],
            ),
            TextArea(title="What are your reasons for this decision?", extras={"max_length": 5000}, name="text"),
            PicklistPicker(target="text", items=get_picklists_for_input(request, "standard_advice")),
            TextArea(
                title="Is there anything else you want to say to the applicant?",
                description="This will appear on the generated documentation",
                optional=True,
                extras={"max_length": 200},
                name="note",
            ),
        ],
        default_button_name=cases.AdviceRecommendationForm.Actions.CONTINUE_BUTTON,
        back_link=BackLink(
            cases.AdviceRecommendationForm.Actions.BACK_BUTTON,
            reverse(f"cases:case", kwargs={"queue_pk": queue_pk, "pk": case["id"], "tab": tab}),
        ),
        # post_url=post_url,
        container="case",
        helpers=[HelpSection("Giving advice on:", "", includes="case/includes/selection-sidebar.html")],
    )


def generate_documents_form():
    return Form(
        "Generate decision documents",
        questions=[Custom("components/finalise-generate-documents.html")],
        container="case",
    )


def finalise_goods_countries_form():
    return Form(
        title="Select a decision for each good and country combination",
        questions=[Custom("components/finalise-goods-countries-table.html")],
        container="case",
    )
