from django.urls import reverse_lazy
from lite_forms.components import Form, TextInput, BackLink, DateInput, Label
from lite_forms.helpers import conditional


def approve_licence_form(case_id, standard, duration, editable_duration):
    return Form(
        title="Approve",
        questions=[
            DateInput(description="For example, 27 3 2007", title="When will the licence start?", prefix=""),
            conditional(
                editable_duration,
                TextInput(
                    name="duration",
                    description="This must be a whole number of months, such as 12",
                    title="How long will it last?",
                ),
                Label(text=f"Duration: {duration} months"),
            ),
        ],
        back_link=conditional(
            standard,
            BackLink(url=reverse_lazy("cases:final_advice_view", kwargs={"pk": case_id}), text="Back to final advice"),
            BackLink(
                url=reverse_lazy("cases:finalise_goods_countries", kwargs={"pk": case_id}),
                text="Back to finalise goods and countries",
            ),
        ),
    )


def refuse_licence_form(case_id, standard):
    return Form(
        title="Refuse",
        back_link=conditional(
            standard,
            BackLink(url=reverse_lazy("cases:final_advice_view", kwargs={"pk": case_id}), text="Back to final advice"),
            BackLink(
                url=reverse_lazy("cases:finalise_goods_countries", kwargs={"pk": case_id}),
                text="Back to finalise goods and countries",
            ),
        ),
    )
