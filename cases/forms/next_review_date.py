from django.urls import reverse

from lite_forms.components import Form, BackLink, DateInput, Button


def set_next_review_date_form(queue_id, case_id):
    return Form(
        title="Set next review date",
        description="For example, 12 11 2020",
        questions=[DateInput(prefix="from_", inline_title=True)],
        buttons=[Button("Continue", action="submit")],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_id, "pk": case_id, "tab": "details"})),
    )