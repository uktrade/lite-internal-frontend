from django.urls import reverse_lazy

from core.services import get_countries
from lite_content.lite_internal_frontend.cases import AddAdditionalContact
from lite_forms.common import country_question
from lite_forms.components import Form, TextInput, Heading, TextArea, BackLink
from lite_forms.styles import HeadingStyle


def add_additional_contact_form(request, case):
    return Form(
        title=AddAdditionalContact.TITLE,
        description=AddAdditionalContact.DESCRIPTION,
        questions=[
            TextInput(title=AddAdditionalContact.Name.TITLE, name="name"),
            TextInput(title=AddAdditionalContact.Email.TITLE, name="email"),
            TextInput(
                title=AddAdditionalContact.PhoneNumber.TITLE,
                description=AddAdditionalContact.PhoneNumber.DESCRIPTION,
                name="phone_number",
            ),
            TextArea(
                title=AddAdditionalContact.Details.TITLE,
                description=AddAdditionalContact.Details.DESCRIPTION,
                name="details",
            ),
            Heading(text=AddAdditionalContact.ADDRESS_HEADING, heading_style=HeadingStyle.M),
            TextArea(
                title=AddAdditionalContact.Address.TITLE,
                description=AddAdditionalContact.Address.DESCRIPTION,
                name="address",
            ),
            country_question(get_countries(request, True), ""),
        ],
        back_link=BackLink(
            AddAdditionalContact.BACK_LINK, reverse_lazy("cases:additional_contacts", kwargs={"pk": case["id"]})
        ),
        default_button_name=AddAdditionalContact.SUBMIT_BUTTON,
    )
