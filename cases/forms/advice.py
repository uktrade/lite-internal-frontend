from django.urls import reverse

from cases.constants import CaseType
from cases.objects import Case
from lite_forms.components import Form, RadioButtons, Option, BackLink
from lite_content.lite_internal_frontend.strings import cases


def advice_recommendation_form(case: Case, tab, queue_pk):
    if case.sub_type == CaseType.OPEN.value:
        denial_option = Option("refuse", cases.AdviceRecommendationForm.RadioButtons.REJECT)
    else:
        denial_option = Option("refuse", cases.AdviceRecommendationForm.RadioButtons.REFUSE)

    return Form(
        cases.AdviceRecommendationForm.TITLE,
        cases.AdviceRecommendationForm.DESCRIPTION,
        [
            RadioButtons(
                "type",
                [
                    Option("approve", cases.AdviceRecommendationForm.RadioButtons.GRANT),
                    Option("proviso", cases.AdviceRecommendationForm.RadioButtons.PROVISO),
                    denial_option,
                    Option("no_licence_required", cases.AdviceRecommendationForm.RadioButtons.NLR),
                    Option("not_applicable", cases.AdviceRecommendationForm.RadioButtons.NOT_APPLICABLE, show_or=True),
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
