from cases.services import get_user_case_queues
from lite_forms.components import Form, Option, Checkboxes


def done_with_case_form(request, case_pk):
    queues, _ = get_user_case_queues(request, case_pk)

    return Form(
        title="Unassign queues",
        questions=[
            Checkboxes(
                name="queues[]",
                options=[Option(queue["id"], queue["name"]) for queue in queues["results"]],
                title="",
                description="Select which queues you are done with this case on",
                optional=False,
            )
        ],
        default_button_name="Submit",
    )
