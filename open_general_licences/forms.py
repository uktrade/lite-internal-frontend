from core.services import get_control_list_entries, get_countries
from lite_content.lite_internal_frontend import generic
from lite_forms.components import (
    Form,
    TreeView,
    FormGroup,
    TextArea,
    RadioButtons,
    Option,
    TextInput,
    Checkboxes,
    Filter,
)
from lite_forms.helpers import convert_dictionary_to_tree
from core.helpers import group_control_list_entries_by_category
from open_general_licences.enums import OpenGeneralExportLicences


def open_general_licence_forms(request, licence, strings):
    control_list_entries = get_control_list_entries(request)
    control_list_entries_tree = convert_dictionary_to_tree(
        group_control_list_entries_by_category(control_list_entries),
        key="rating",
        value="rating",
        exclude="is_decontrolled",
    )
    countries = get_countries(request, True)

    return FormGroup(
        [
            Form(
                title=strings.SelectType.TITLE,
                description=strings.SelectType.DESCRIPTION,
                caption="Step 1 of 4",
                questions=[
                    RadioButtons(short_title="Type", name="case_type", options=OpenGeneralExportLicences.as_options(),),
                ],
                default_button_name=generic.CONTINUE,
            ),
            Form(
                title=strings.Details.TITLE.format(licence.name.lower()),
                description=strings.Details.DESCRIPTION,
                caption="Step 2 of 4",
                questions=[
                    TextArea(
                        title=strings.Details.Name.TITLE.format(licence.name.lower()),
                        short_title=strings.Details.Name.SHORT_TITLE,
                        description=strings.Details.Name.DESCRIPTION,
                        name="name",
                        rows=3,
                        classes=["govuk-!-width-three-quarters"],
                        data_attributes={"licence-name": licence.name},
                    ),
                    TextArea(
                        title=strings.Details.Description.TITLE,
                        short_title=strings.Details.Description.SHORT_TITLE,
                        description=strings.Details.Description.DESCRIPTION,
                        name="description",
                        classes=["govuk-!-width-three-quarters"],
                        extras={"max_length": 2000},
                    ),
                    TextInput(
                        title=strings.Details.Link.TITLE.format(licence.name.lower()),
                        short_title=strings.Details.Link.SHORT_TITLE,
                        description=strings.Details.Link.DESCRIPTION,
                        name="url",
                        classes=["govuk-!-width-three-quarters"],
                    ),
                    RadioButtons(
                        title=strings.Details.RequiresRegistration.TITLE.format(licence.name.lower()),
                        short_title=strings.Details.RequiresRegistration.SHORT_TITLE,
                        description=strings.Details.RequiresRegistration.DESCRIPTION.format(licence.name.lower()),
                        name="registration_required",
                        options=[Option(True, "Yes"), Option(False, "No"),],
                        classes=["govuk-radios--inline"],
                    ),
                ],
                javascript_imports=["/assets/javascripts/new-open-general-licence.js"],
                default_button_name=generic.CONTINUE,
            ),
            Form(
                title=strings.ControlListEntries.TITLE,
                description=strings.ControlListEntries.DESCRIPTION,
                caption="Step 3 of 4",
                questions=[
                    TreeView(
                        name="control_list_entries[]",
                        title="",
                        short_title="Control list entries",
                        data=control_list_entries_tree,
                    )
                ],
                default_button_name=generic.CONTINUE,
            ),
            Form(
                title=strings.Countries.TITLE,
                description=strings.Countries.DESCRIPTION,
                caption="Step 4 of 4",
                questions=[
                    Filter(),
                    Checkboxes(
                        name="countries[]",
                        short_title="Countries",
                        options=countries,
                        classes=["govuk-checkboxes--small"],
                    ),
                ],
                default_button_name=generic.CONTINUE,
                javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
            ),
        ]
    )
