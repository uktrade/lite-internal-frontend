from django.urls import reverse

from lite_forms.generators import confirm_form


def reissue_ogel_confirmation_form(case_id, queue_id):
    return confirm_form(
        title="Do you want to reissue this OGEL?",
        description="Doing so will allow the exporter to resume using this OGEL",
        confirmation_name="confirm",
        back_link_text="Back",
        back_url=reverse("cases:case", kwargs={"queue_pk": queue_id, "pk": case_id}),
        yes_label="Yes",
        no_label="No",
        submit_button_text="Submit",
        container="case",
    )
