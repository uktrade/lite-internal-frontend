from django.urls import reverse

from conf.constants import Permission
from lite_content.lite_internal_frontend import strings
from lite_content.lite_internal_frontend.organisations import RegisterAnOrganisation
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

from core.services import get_countries, get_user_permissions


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
                title=RegisterAnOrganisation.COMMERCIAL_OR_PRIVATE_INDIVIDUAL,
                questions=[
                    RadioButtons(
                        name="type",
                        options=[
                            Option(key="commercial", value="Commercial"),
                            Option(key="individual", value="Individual"),
                        ],
                    )
                ],
                back_link=BackLink(RegisterAnOrganisation.BACK_LINK, reverse("organisations:organisations")),
                default_button_name=strings.CONTINUE,
            ),
            Form(
                title="Where is the organisation based?",
                questions=[
                    RadioButtons(
                        name="location",
                        options=[
                            Option(key="united_kingdom", value="In the United Kingdom"),
                            Option(key="individual", value="Outside of the United Kingdom"),
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
        title=RegisterAnOrganisation.COMMERCIAL_TITLE,
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


# def register_hmrc_organisation_forms():
#     return FormGroup(
#         [
#             Form(
#                 title="Register an HMRC organisation",
#                 questions=[
#                     HiddenField(name="type", value="hmrc"),
#                     TextInput(title="Name of HMRC organisation", name="name"),
#                     TextInput(title=RegisterAnOrganisation.NAME_OF_SITE, name="site.name"),
#                     Heading("Where are they based?", HeadingStyle.M),
#                     *address_questions(get_countries(None, True), "site.address."),
#                 ],
#                 default_button_name="Continue",
#             ),
#             create_admin_user_form(),
#         ],
#         show_progress_indicators=True,
#     )


# def edit_individual_form(permission_to_edit_org_name):
#     return Form(
#         title=RegisterAnOrganisation.EDIT_INDIVIDUAL_TITLE,
#         questions=[
#             conditional(
#                 permission_to_edit_org_name, TextInput(title=REGISTER_BUSINESS_FIRST_AND_LAST_NAME, name="name"),
#             ),
#             TextInput(title=RegisterAnOrganisation.EMAIL, name="user.email"),
#             TextInput(title=RegisterAnOrganisation.EORI_NUMBER, name="eori_number"),
#             TextInput(
#                 title=RegisterAnOrganisation.UkVatNumber.TITLE,
#                 description=RegisterAnOrganisation.UkVatNumber.DESCRIPTION,
#                 optional=True,
#                 name="vat_number",
#             ),
#         ],
#         default_button_name=strings.CONTINUE,
#     )
#
#
# def edit_commercial_form(permission_to_edit_org_name):
#     return Form(
#         title=RegisterAnOrganisation.EDIT_COMMERCIAL_TITLE,
#         questions=[
#             conditional(
#                 permission_to_edit_org_name, TextInput(title=REGISTER_BUSINESS_FIRST_AND_LAST_NAME, name="name"),
#             ),
#             TextInput(title=RegisterAnOrganisation.EORI_NUMBER, name="eori_number"),
#             TextInput(
#                 title=RegisterAnOrganisation.SicNumber.TITLE,
#                 description=RegisterAnOrganisation.SicNumber.DESCRIPTION,
#                 name="sic_number",
#             ),
#             TextInput(
#                 title=RegisterAnOrganisation.UkVatNumber.TITLE,
#                 description=RegisterAnOrganisation.UkVatNumber.DESCRIPTION,
#                 name="vat_number",
#             ),
#             TextInput(
#                 title=RegisterAnOrganisation.CRN,
#                 description=RegisterAnOrganisation.CRN_DESCRIPTION,
#                 name="registration_number",
#             ),
#         ],
#         default_button_name=CONTINUE,
#     )


# def edit_business_forms(request, individual=False):
#     user_permissions = get_user_permissions(request)
#     permission_to_edit_org_name = (
#         Permission.MANAGE_ORGANISATIONS.value in user_permissions
#         and Permission.REOPEN_CLOSED_CASES.value in user_permissions
#     )
#
#     return FormGroup(
#         [
#             individual_or_commercial(),
#             conditional(
#                 individual,
#                 edit_individual_form(permission_to_edit_org_name),
#                 edit_commercial_form(permission_to_edit_org_name),
#             ),
#         ],
#         show_progress_indicators=True,
#     )
