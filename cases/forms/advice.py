from cases.constants import CaseType
from lite_forms.components import Form, RadioButtons, Option, BackLink
from lite_content.lite_internal_frontend.strings import cases


def advice_recommendation_form(post_url, back_url, application_type):
    if application_type == CaseType.OPEN_LICENCE:
        denial_option = Option("refuse", "Reject the licence")
    else:
        denial_option = Option("refuse", "Refuse the licence")

    return Form(
        cases.AdviceRecommendationForm.TITLE,
        cases.AdviceRecommendationForm.DESCRIPTION,
        [
            RadioButtons(
                "type",
                [
                    Option("approve", "Grant the licence"),
                    Option("proviso", "Add a proviso"),
                    denial_option,
                    Option("no_licence_required", "Tell the applicant they do not need a licence"),
                    Option("not_applicable", "Not applicable", show_or=True),
                ],
            ),
        ],
        default_button_name=cases.AdviceRecommendationForm.Actions.CONTINUE_BUTTON,
        back_link=BackLink(cases.AdviceRecommendationForm.Actions.BACK_BUTTON, back_url),
        post_url=post_url,
    )
