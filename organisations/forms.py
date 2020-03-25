from django.urls import reverse

from core.services import get_countries
from lite_content.lite_internal_frontend import strings
from lite_content.lite_internal_frontend.organisations import (
    RegisterAnOrganisation,
    EditIndividualOrganisationPage,
    EditCommercialOrganisationPage,
)
from lite_forms.common import address_questions, foreign_address_questions
from lite_forms.components import (
    Form,
    TextInput,
    Heading,
    HelpSection,
    FormGroup,
    Option,
    RadioButtons,
    HiddenField,
    BackLink,
    EmailInput,
)
from lite_forms.helpers import conditional
from lite_forms.styles import HeadingStyle


def register_organisation_forms(request):
    """
    Handles flow for registering an organisation
    Diverges based on organisation type (individual or commercial), location answer
    also changes compulsory fields
    """
    is_individual = request.POST.get("type") == "individual"
    in_uk = request.POST.get("location") == "united_kingdom"

    return FormGroup(
        [
            Form(
                title=RegisterAnOrganisation.CommercialOrIndividual.TITLE,
                description=RegisterAnOrganisation.CommercialOrIndividual.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="type",
                        options=[
                            Option(
                                key="commercial",
                                value=RegisterAnOrganisation.CommercialOrIndividual.COMMERCIAL_TITLE,
                                description=RegisterAnOrganisation.CommercialOrIndividual.COMMERCIAL_DESCRIPTION,
                            ),
                            Option(
                                key="individual",
                                value=RegisterAnOrganisation.CommercialOrIndividual.INDIVIDUAL_TITLE,
                                description=RegisterAnOrganisation.CommercialOrIndividual.INDIVIDUAL_DESCRIPTION,
                            ),
                        ],
                    )
                ],
                back_link=BackLink(RegisterAnOrganisation.BACK_LINK, reverse("organisations:organisations")),
                default_button_name=strings.CONTINUE,
            ),
            Form(
                title=RegisterAnOrganisation.WhereIsTheExporterBased.TITLE,
                description=RegisterAnOrganisation.WhereIsTheExporterBased.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="location",
                        options=[
                            Option(
                                key="united_kingdom",
                                value=RegisterAnOrganisation.WhereIsTheExporterBased.IN_THE_UK_TITLE,
                                description=RegisterAnOrganisation.WhereIsTheExporterBased.IN_THE_UK_DESCRIPTION,
                            ),
                            Option(
                                key="abroad",
                                value=RegisterAnOrganisation.WhereIsTheExporterBased.ABROAD_TITLE,
                                description=RegisterAnOrganisation.WhereIsTheExporterBased.ABROAD_DESCRIPTION,
                            ),
                        ],
                    )
                ],
                default_button_name=strings.CONTINUE,
            ),
            conditional(is_individual, register_individual_form(in_uk), register_commercial_form(in_uk)),
            create_default_site_form(in_uk),
            conditional(not is_individual, create_admin_user_form(),),
        ],
        show_progress_indicators=True,
    )


def register_individual_form(in_uk):
    return Form(
        title=RegisterAnOrganisation.INDIVIDUAL_TITLE,
        questions=[
            TextInput(
                title=RegisterAnOrganisation.IndividualName.TITLE,
                description=RegisterAnOrganisation.IndividualName.DESCRIPTION,
                name="name",
            ),
            EmailInput(title=RegisterAnOrganisation.EMAIL, name="user.email"),
            TextInput(
                title=RegisterAnOrganisation.EORINumber.TITLE,
                description=RegisterAnOrganisation.EORINumber.DESCRIPTION,
                name="eori_number",
                optional=not in_uk,
            ),
            TextInput(
                title=RegisterAnOrganisation.UkVatNumber.TITLE,
                description=RegisterAnOrganisation.UkVatNumber.DESCRIPTION,
                optional=True,
                name="vat_number",
            ),
        ],
        default_button_name=strings.CONTINUE,
    )


def register_commercial_form(in_uk):
    return Form(
        title=RegisterAnOrganisation.COMMERCIAL_TITLE,
        questions=[
            TextInput(
                title=RegisterAnOrganisation.Name.TITLE,
                description=RegisterAnOrganisation.Name.DESCRIPTION,
                name="name",
            ),
            TextInput(
                title=RegisterAnOrganisation.EORINumber.TITLE,
                description=RegisterAnOrganisation.EORINumber.DESCRIPTION,
                name="eori_number",
                optional=not in_uk,
            ),
            TextInput(
                title=RegisterAnOrganisation.SicNumber.TITLE,
                description=RegisterAnOrganisation.SicNumber.DESCRIPTION,
                name="sic_number",
                optional=not in_uk,
            ),
            TextInput(
                title=RegisterAnOrganisation.UkVatNumber.TITLE,
                description=RegisterAnOrganisation.UkVatNumber.DESCRIPTION,
                name="vat_number",
                optional=not in_uk,
            ),
            TextInput(
                title=RegisterAnOrganisation.RegistrationNumber.TITLE,
                description=RegisterAnOrganisation.RegistrationNumber.DESCRIPTION,
                name="registration_number",
                optional=not in_uk,
            ),
        ],
        default_button_name=strings.CONTINUE,
    )


def create_default_site_form(in_uk):
    return Form(
        title=RegisterAnOrganisation.CREATE_DEFAULT_SITE,
        questions=[
            TextInput(title=RegisterAnOrganisation.NAME_OF_SITE, name="site.name"),
            Heading(RegisterAnOrganisation.WHERE_IS_THE_EXPORTER_BASED, HeadingStyle.M),
            *conditional(
                in_uk,
                address_questions(None, "site.address."),
                foreign_address_questions(get_countries(None, True), "site.foreign_address."),
            ),
        ],
        default_button_name=strings.CONTINUE,
    )


def create_admin_user_form():
    return Form(
        title="Create an admin user for this organisation",
        questions=[TextInput(title=RegisterAnOrganisation.EMAIL, name="user.email"),],
        default_button_name="Submit",
        helpers=[HelpSection("Help", RegisterAnOrganisation.DEFAULT_USER)],
    )


def register_hmrc_organisation_forms():
    return FormGroup(
        [
            Form(
                title="Register an HMRC organisation",
                questions=[
                    HiddenField(name="type", value="hmrc"),
                    TextInput(title="Name of HMRC organisation", name="name"),
                    TextInput(title=RegisterAnOrganisation.NAME_OF_SITE, name="site.name"),
                    Heading("Where are they based?", HeadingStyle.M),
                    *address_questions(None, "site.address."),
                ],
                default_button_name="Continue",
            ),
            create_admin_user_form(),
        ],
        show_progress_indicators=True,
    )


def edit_commercial_form(organisation, can_edit_name, are_fields_optional):
    return Form(
        title=EditCommercialOrganisationPage.TITLE,
        questions=[
            conditional(
                can_edit_name,
                TextInput(
                    title=EditCommercialOrganisationPage.Name.TITLE,
                    description=EditCommercialOrganisationPage.Name.DESCRIPTION,
                    name="name",
                ),
            ),
            TextInput(
                title=EditCommercialOrganisationPage.EORINumber.TITLE,
                description=EditCommercialOrganisationPage.EORINumber.DESCRIPTION,
                name="eori_number",
                optional=are_fields_optional,
            ),
            TextInput(
                title=EditCommercialOrganisationPage.SICNumber.TITLE,
                description=EditCommercialOrganisationPage.SICNumber.DESCRIPTION,
                name="sic_number",
                optional=are_fields_optional,
            ),
            TextInput(
                title=EditCommercialOrganisationPage.VATNumber.TITLE,
                description=EditCommercialOrganisationPage.VATNumber.DESCRIPTION,
                name="vat_number",
                optional=are_fields_optional,
            ),
            TextInput(
                title=EditCommercialOrganisationPage.RegistrationNumber.TITLE,
                description=EditCommercialOrganisationPage.RegistrationNumber.DESCRIPTION,
                name="registration_number",
                optional=are_fields_optional,
            ),
        ],
        back_link=BackLink(
            EditCommercialOrganisationPage.BACK_LINK,
            reverse("organisations:organisation", kwargs={"pk": organisation["id"]}),
        ),
        default_button_name=EditIndividualOrganisationPage.SUBMIT_BUTTON,
    )


def edit_individual_form(organisation, can_edit_name, are_fields_optional):
    return Form(
        title=EditIndividualOrganisationPage.TITLE,
        questions=[
            conditional(
                can_edit_name,
                TextInput(
                    title=EditIndividualOrganisationPage.Name.TITLE,
                    description=EditIndividualOrganisationPage.Name.DESCRIPTION,
                    name="name",
                ),
            ),
            TextInput(
                title=EditIndividualOrganisationPage.EORINumber.TITLE,
                description=EditIndividualOrganisationPage.Name.DESCRIPTION,
                name="eori_number",
                optional=are_fields_optional,
            ),
            TextInput(
                title=EditIndividualOrganisationPage.VATNumber.TITLE,
                description=EditIndividualOrganisationPage.VATNumber.DESCRIPTION,
                optional=True,
                name="vat_number",
            ),
        ],
        back_link=BackLink(
            EditIndividualOrganisationPage.BACK_LINK,
            reverse("organisations:organisation", kwargs={"pk": organisation["id"]}),
        ),
        default_button_name=EditIndividualOrganisationPage.SUBMIT_BUTTON,
    )
