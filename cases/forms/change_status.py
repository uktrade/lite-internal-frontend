from cases.helpers import case_view_breadcrumbs
from lite_content.lite_internal_frontend import cases
from lite_forms.components import Form, RadioButtons, Option


def change_status_form(case, statuses):
    return Form(
        title=cases.ChangeStatusPage.TITLE,
        description=cases.ChangeStatusPage.DESCRIPTION,
        questions=[
            RadioButtons(
                name="status",
                options=[Option(status["key"], status["value"]) for status in statuses],
                classes=["govuk-radios--small"],
            )
        ],
        back_link=case_view_breadcrumbs(case, cases.ChangeStatusPage.TITLE),
    )
