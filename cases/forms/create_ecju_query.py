from django.urls import reverse

from core.components import PicklistPicker
from lite_content.lite_internal_frontend.strings import cases
from lite_forms.components import Form, BackLink, TextArea, RadioButtons, FormGroup, Option
from picklists.services import get_picklists_list, get_picklists_for_input


class ECJUQueryTypes:
    ECJU_QUERY = "ecju_query"
    PRE_VISIT_QUESTIONNAIRE = "pre_visit_questionnaire"
    COMPLIANCE_ACTION = "compliance_actions"

    choices = [
        (ECJU_QUERY, "Standard query"),
        (PRE_VISIT_QUESTIONNAIRE, "Pre-visit questionnaire query"),
        (COMPLIANCE_ACTION, "Compliance query"),
    ]

    @classmethod
    def get_text(cls, choice):
        for key, value in cls.choices:
            if key == choice:
                return value
        return ""


def new_ecju_query_form(request, queue_pk, pk):
    query_type = request.POST.get("query_type", "")
    return FormGroup(
        [
            Form(
                title=cases.EcjuQueries.AddQuery.CHOOSE_TYPE,
                questions=[
                    RadioButtons(
                        name="query_type",
                        options=[Option(choice[0], choice[1]) for choice in ECJUQueryTypes.choices],
                    )
                ],
                back_link=BackLink(
                    url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "ecju-queries"})
                ),
                default_button_name="Continue",
                container="case",
            ),
            Form(
                title="New " + ECJUQueryTypes.get_text(query_type).lower(),
                questions=[
                    TextArea(
                        description=cases.EcjuQueries.AddQuery.DESCRIPTION,
                        name="question",
                        extras={"max_length": 5000,},
                        data_attributes={"picklist-picker": query_type}
                    ),
                    PicklistPicker(name="question",
                                   items=get_picklists_for_input(request, query_type)),
                ],
                default_button_name="Send",
                container="case",
            ),
        ]
    )
