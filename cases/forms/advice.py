from django.urls import reverse

from cases.constants import CaseType
from cases.objects import Case
from lite_forms.components import Form, RadioButtons, Option, BackLink, Summary
from lite_content.lite_internal_frontend.strings import cases
from lite_forms.helpers import conditional


def give_advice_form(case: Case, tab, queue_pk):
    return Form(
        title=cases.AdviceRecommendationForm.TITLE,
        questions=[
            Summary({"Goods": "ML1a, ML2, PL10123", "Destinations": "Poland, United Kingdom"}),
            RadioButtons(
                description=cases.AdviceRecommendationForm.DESCRIPTION,
                name="type",
                options=[
                    Option(key="approve", value=cases.AdviceRecommendationForm.RadioButtons.GRANT),
                    Option(key="proviso", value=cases.AdviceRecommendationForm.RadioButtons.PROVISO),
                    Option(
                        key="refuse",
                        value=conditional(
                            case.sub_type == CaseType.OPEN.value,
                            cases.AdviceRecommendationForm.RadioButtons.REJECT,
                            cases.AdviceRecommendationForm.RadioButtons.REFUSE,
                        ),
                    ),
                    Option(key="no_licence_required", value=cases.AdviceRecommendationForm.RadioButtons.NLR),
                    Option(
                        key="not_applicable",
                        value=cases.AdviceRecommendationForm.RadioButtons.NOT_APPLICABLE,
                        show_or=True,
                    ),
                ],
            ),
        ],
        default_button_name=cases.AdviceRecommendationForm.Actions.CONTINUE_BUTTON,
        back_link=BackLink(
            cases.AdviceRecommendationForm.Actions.BACK_BUTTON,
            reverse(f"cases:case", kwargs={"queue_pk": queue_pk, "pk": case["id"], "tab": tab}),
        ),
        # post_url=post_url,
        container="case",
    )
