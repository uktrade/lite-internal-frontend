from lite_forms.components import Form, Option, Checkboxes


def done_with_case_form(request, case_pk):
    queues = {"1": "MyQueue"}

    return Form(
        title="Assigned queues",
        questions=[
            Checkboxes(
                name="queues[]",
                options=[Option(key, value) for key, value in queues.items()],
                title="",
                description="Select which queues you are done with this case on",
                optional=False,
            )
        ],
        default_button_name="Submit",
    )
