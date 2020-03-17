from django.urls import reverse_lazy

from core.services import get_countries
from lite_forms.common import address_questions
from lite_forms.components import Form, TextInput, Heading, TextArea, BackLink
from lite_forms.styles import HeadingStyle


def add_additional_contact_form(request, case):
    return Form(
        title="Add an additional contact",
        description="",
        questions=[
            TextInput(title="Full name", name="name"),
            TextInput(title="Email address", name="email"),
            TextInput(
                title="Telephone number",
                description="For international numbers include the country code",
                name="phone_number",
            ),
            Heading(text="Address", heading_style=HeadingStyle.M),
            *address_questions(get_countries(request, True)),
            TextArea(title="Enter any other details about this contact", description="Include ??", name="details"),
        ],
        back_link=BackLink(
            "Back to additional contacts", reverse_lazy("cases:additional_contacts", kwargs={"pk": case["id"]})
        ),
        default_button_name="Save and continue",
    )
