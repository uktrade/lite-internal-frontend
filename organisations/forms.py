from conf.constants import Permission
from lite_content.lite_internal_frontend import strings
from lite_forms.common import address_questions
from lite_forms.components import (
    Form,
    TextInput,
    Heading,
    HelpSection,
    FormGroup,
    Option,
    RadioButtons,
    HiddenField,
)
from lite_forms.helpers import conditional
from lite_forms.styles import HeadingStyle

from core.services import get_countries, get_user_permissions


def register_business_forms(individual=False, name=""):

    return FormGroup(
        [
            individual_or_commerical_form,
            conditional(
                individual,
                Form(
                    title=strings.RegisterBusiness.REGISTER_INDIVIDUAL_TITLE,
                    questions=[
                        TextInput(title=strings.REGISTER_BUSINESS_FIRST_AND_LAST_NAME, name="name"),
                        TextInput(title=strings.RegisterBusiness.EMAIL, name="user.email"),
                        TextInput(title=strings.RegisterBusiness.EORI_NUMBER, name="eori_number"),
                        TextInput(
                            title=strings.RegisterBusiness.UkVatNumber.TITLE,
                            description=strings.RegisterBusiness.UkVatNumber.DESCRIPTION,
                            optional=True,
                            name="vat_number",
                        ),
                    ],
                    default_button_name=strings.CONTINUE,
                ),
                Form(
                    title=strings.RegisterBusiness.REGISTER_COMMERCIAL_TITLE,
                    questions=[
                        TextInput(title=strings.RegisterBusiness.NAME, name="name"),
                        TextInput(title=strings.RegisterBusiness.EORI_NUMBER, name="eori_number"),
                        TextInput(
                            title=strings.RegisterBusiness.SIC_NUMBER,
                            description="Classifies industries by a four-digit code.",
                            name="sic_number",
                        ),
                        TextInput(
                            title=strings.RegisterBusiness.UkVatNumber.TITLE,
                            description=strings.RegisterBusiness.UkVatNumber.DESCRIPTION,
                            name="vat_number",
                        ),
                        TextInput(
                            title=strings.RegisterBusiness.CRN,
                            description=strings.RegisterBusiness.CRN_DESCRIPTION,
                            name="registration_number",
                        ),
                    ],
                    default_button_name=strings.CONTINUE,
                ),
            ),
            Form(
                title=strings.RegisterBusiness.CREATE_DEFAULT_SITE,
                questions=[
                    TextInput(title=strings.RegisterBusiness.NAME_OF_SITE, name="site.name"),
                    Heading(strings.RegisterBusiness.WHERE_IS_THE_EXPORTER_BASED, HeadingStyle.M),
                    *address_questions(get_countries(None, True), "site.address."),
                ],
                default_button_name=strings.CONTINUE,
            ),
            add_admin_user_form(individual, name),
        ],
        show_progress_indicators=True,
    )


def register_hmrc_organisation_forms(name=""):
    return FormGroup(
        [
            Form(
                title="Register an HMRC organisation",
                questions=[
                    HiddenField(name="type", value="hmrc"),
                    TextInput(title="Name of HMRC organisation", name="name"),
                    TextInput(title=strings.RegisterBusiness.NAME_OF_SITE, name="site.name"),
                    Heading("Where are they based?", HeadingStyle.M),
                    *address_questions(get_countries(None, True), "site.address."),
                ],
                default_button_name="Continue",
            ),
            Form(
                title="Create an admin for " + name,
                questions=[TextInput(title=strings.RegisterBusiness.EMAIL, name="user.email"),],
                default_button_name="Submit",
                helpers=[HelpSection("Help", strings.RegisterBusiness.DEFAULT_USER)],
            ),
        ],
        show_progress_indicators=True,
    )


def individual_or_commerical_form():
    return Form(
        title=strings.RegisterBusiness.COMMERCIAL_OR_PRIVATE_INDIVIDUAL,
        questions=[
            RadioButtons(
                name="type",
                options=[Option(key="commercial", value="Commercial"), Option(key="individual", value="Individual"),],
            )
        ],
        default_button_name=strings.CONTINUE,
    )


def add_admin_user_form(individual, name):
    return conditional(
        not individual,
        Form(
            title="Create an admin user for " + name,
            questions=[TextInput(title=strings.RegisterBusiness.EMAIL, name="user.email"),],
            default_button_name="Submit",
            helpers=[HelpSection("Help", strings.RegisterBusiness.DEFAULT_USER)],
        ),
    )


def edit_business_forms(request, individual=False, name=""):
    user_permissions = get_user_permissions(request)
    permission_to_edit_org_name = (
        Permission.MANAGE_ORGANISATIONS.value in user_permissions
        and Permission.REOPEN_CLOSED_CASES.value in user_permissions
    )
    return FormGroup(
        [
            individual_or_commerical_form(),
            conditional(
                individual,
                Form(
                    title=strings.RegisterBusiness.EDIT_INDIVIDUAL_TITLE,
                    questions=[
                        conditional(
                            permission_to_edit_org_name,
                            TextInput(title=strings.REGISTER_BUSINESS_FIRST_AND_LAST_NAME, name="name"),
                        ),
                        TextInput(title=strings.RegisterBusiness.EMAIL, name="user.email"),
                        TextInput(title=strings.RegisterBusiness.EORI_NUMBER, name="eori_number"),
                        TextInput(
                            title=strings.RegisterBusiness.UkVatNumber.TITLE,
                            description=strings.RegisterBusiness.UkVatNumber.DESCRIPTION,
                            optional=True,
                            name="vat_number",
                        ),
                    ],
                    default_button_name=strings.CONTINUE,
                ),
                Form(
                    title=strings.RegisterBusiness.EDIT_COMMERCIAL_TITLE,
                    questions=[
                        conditional(
                            permission_to_edit_org_name,
                            TextInput(title=strings.REGISTER_BUSINESS_FIRST_AND_LAST_NAME, name="name"),
                        ),
                        TextInput(title=strings.RegisterBusiness.EORI_NUMBER, name="eori_number"),
                        TextInput(
                            title=strings.RegisterBusiness.SIC_NUMBER,
                            description="Classifies industries by a four-digit code.",
                            name="sic_number",
                        ),
                        TextInput(
                            title=strings.RegisterBusiness.UkVatNumber.TITLE,
                            description=strings.RegisterBusiness.UkVatNumber.DESCRIPTION,
                            name="vat_number",
                        ),
                        TextInput(
                            title=strings.RegisterBusiness.CRN,
                            description=strings.RegisterBusiness.CRN_DESCRIPTION,
                            name="registration_number",
                        ),
                    ],
                    default_button_name=strings.CONTINUE,
                ),
            ),
            add_admin_user_form(individual, name),
        ],
        show_progress_indicators=True,
    )
