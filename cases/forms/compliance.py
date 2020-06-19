from django.urls import reverse

from lite_forms.components import Form, BackLink, DateInput, Select, Option, TextArea

Visit_type_choices = [
    Option("first_contact", "First contact"),
    Option("first_visit", "First visit"),
    Option("routine_visit", "Routine visit"),
    Option("revisit", "Revisit"),
]

risk_value = [
    Option("very_low", "Very low risk"),
    Option("lower", "Lower risk"),
    Option("medium", "Medium risk"),
    Option("higher", "Higher risk"),
    Option("highest", "Highest risk"),
]


def visit_report_form(queue_pk, pk):
    return Form(
        title="Visit report details",
        questions=[
            Select(title="Visit type", name="visit_type", options=Visit_type_choices),
            DateInput(
                title="Visit date", description="For example, 12 3 2020", name="visit_date", prefix="visit_date_"
            ),
            Select(title="Overall risk value", name="overall_risk_value", options=risk_value),
            Select(
                title="Licence risk value",
                name="licence_risk_value",
                options=[Option(str(i), str(i)) for i in range(1, 5)],
            ),
        ],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "details"})),
    )


def overview_form(queue_pk, pk):
    return Form(
        title="Overview",
        questions=[TextArea(name="overview")],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "details"})),
    )


def inspection_form(queue_pk, pk):
    return Form(
        title="Inspection",
        questions=[TextArea(name="inspection")],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "details"})),
    )


def compliance_with_licence_form(queue_pk, pk):
    return Form(
        title="Compliance with licence",
        questions=[
            TextArea(title="Overview", name="compliance_overview"),
            Select(title="Risk value", name="compliance_risk_value", options=risk_value),
        ],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "details"})),
    )


def knowledge_of_people_form(queue_pk, pk):
    return Form(
        title="Knowledge and Understanding demonstrated by key export individuals at meeting",
        questions=[
            TextArea(title="Overview", name="individuals_overview"),
            Select(title="Risk value", name="individuals_risk_value", options=risk_value),
        ],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "details"})),
    )


def knowledge_of_products_form(queue_pk, pk):
    return Form(
        title="Knowledge of controlled items in their business' products",
        questions=[
            TextArea(title="Overview", name="products_overview"),
            Select(title="Risk value", name="products_risk_value", options=risk_value),
        ],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": pk, "tab": "details"})),
    )
