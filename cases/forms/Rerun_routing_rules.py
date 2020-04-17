from lite_forms.generators import confirm_form


def rerun_routing_rules_confirmation_form():
    return confirm_form(
        title="Do you want to rerun routing rules?",
        confirmation_name="confirm",
        back_link_text="Back to case",
        back_url="#",
        yes_label="Yes, rerun",
        no_label="Cancel",
        submit_button_text="Continue",
    )
