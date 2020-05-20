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
from lite_forms.helpers import convert_list_to_tree
from open_general_licences.enums import OpenGeneralExportLicences


def new_open_general_licence_forms(request):
    control_list_entries = get_control_list_entries(request)
    control_list_entries_tree = convert_list_to_tree(
        control_list_entries, key="id", value="rating", exclude="is_decontrolled"
    )
    countries = get_countries(request, True)
    licence = OpenGeneralExportLicences.get_by_type(request.POST.get("type", "open_general_export_licence"))

    return FormGroup(
        [
            Form(
                title="Select the type of open general licence you want to add",
                caption="Step 1 of 4",
                questions=[
                    RadioButtons(short_title="Type", name="type", options=OpenGeneralExportLicences.as_options(),),
                ],
                default_button_name=generic.CONTINUE,
            ),
            Form(
                title="Add an open general licence",
                caption="Step 2 of 4",
                questions=[
                    TextArea(
                        title=f"What's the name of the {licence.name.lower()} you want to add?",
                        short_title="Name",
                        description="Use the name from GOV.UK. For example, 'Military goods, software and technology: government or NATO end use'",
                        name="name",
                        rows=3,
                        classes=["govuk-!-width-three-quarters"],
                        data_attributes={"licence-name": licence.name},
                    ),
                    TextInput(
                        title=f"Link to the {licence.name.lower()}",
                        short_title="Link",
                        description="Only link to GOV.UK pages. For example, 'https://www.gov.uk/government/publications/open-general-export-licence-military-goods-government-or-nato-end-use--6'",
                        name="url",
                        classes=["govuk-!-width-three-quarters"],
                    ),
                    TextArea(
                        title="Description",
                        description="Use the description provided by GOV.UK (if possible)",
                        name="description",
                        classes=["govuk-!-width-three-quarters"],
                        extras={"max_length": 2000},
                    ),
                    RadioButtons(
                        title=f"Does this {licence.name.lower()} require registration?",
                        short_title="Requires registration",
                        description=f"Select 'Yes' if an exporter has to register the {licence.name.lower()} to use it",
                        name="name",
                        options=[Option(True, "Yes"), Option(False, "No"),],
                        classes=["govuk-radios--inline"],
                    ),
                ],
                javascript_imports=["/assets/javascripts/new-open-general-licence.js"],
                default_button_name=generic.CONTINUE,
            ),
            Form(
                title="Select control list entries",
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
                title="Select countries",
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
