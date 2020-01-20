from lite_forms.components import Form, RadioButtons, Option, BackLink


def advice_recommendation_form(post_url, back_url, case_type):
    if case_type == "open_licence":
        denial_option = Option("refuse", "Reject the licence")
    else:
        denial_option = Option("refuse", "Refuse the licence")

    return Form(
        "What do you advise?",
        "You can advise to:",
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
        default_button_name="Continue",
        back_link=BackLink("Back to advice", back_url),
        post_url=post_url,
    )
