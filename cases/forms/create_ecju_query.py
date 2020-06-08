from core.components import PicklistPicker
from lite_content.lite_internal_frontend.cases import EcjuQueries
from lite_content.lite_internal_frontend.strings import cases
from lite_forms.components import Form, TextArea, HiddenField


class ECJUQueryTypes:
    ECJU_QUERY = "ecju_query"
    PRE_VISIT_QUESTIONNAIRE = "pre_visit_questionnaire"
    COMPLIANCE_ACTION = "compliance_actions"

    choices = [
        (ECJU_QUERY, EcjuQueries.Queries.ECJU_QUERY),
        (PRE_VISIT_QUESTIONNAIRE, EcjuQueries.Queries.PRE_VISIT_QUESTIONNAIRE),
        (COMPLIANCE_ACTION, EcjuQueries.Queries.COMPLIANCE_ACTION),
    ]

    @classmethod
    def get_text(cls, choice):
        for key, value in cls.choices:
            if key == choice:
                return value
        return ""


def new_ecju_query_form():
    return Form(
        title=EcjuQueries.AddQuery.TITLE_PREFIX + ECJUQueryTypes.get_text(ECJUQueryTypes.ECJU_QUERY).lower(),
        questions=[
            HiddenField("query_type", ECJUQueryTypes.ECJU_QUERY),
            TextArea(
                description=cases.EcjuQueries.AddQuery.DESCRIPTION, name="question", extras={"max_length": 5000,},
            ),
            PicklistPicker(target="question", type=ECJUQueryTypes.ECJU_QUERY),
        ],
        default_button_name=cases.EcjuQueries.AddQuery.SUBMIT,
        container="case",
    )
