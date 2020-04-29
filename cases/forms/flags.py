from cases.helpers import case_view_breadcrumbs
from lite_content.lite_internal_frontend.flags import SetCaseFlagsForm, SetGenericFlagsForm
from lite_forms.components import Form, Filter, Checkboxes, TextArea, BackLink, DetailComponent, TokenBar, Label


def flags_form(flags, level, origin, url):
    return Form(
        title=SetGenericFlagsForm.TITLE,
        description=SetGenericFlagsForm.DESCRIPTION,
        questions=[
            Filter(placeholder=SetGenericFlagsForm.Filter.PLACEHOLDER),
            Checkboxes(name="flags", options=flags),
            TextArea(
                name="note",
                title=SetGenericFlagsForm.Note.TITLE,
                description=SetGenericFlagsForm.Note.DESCRIPTION + level,
                optional=True,
            ),
        ],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        back_link=BackLink(SetGenericFlagsForm.BACK + origin, url),
    )


def set_case_flags_form(queue, flags, case):
    return Form(
        title=SetCaseFlagsForm.TITLE,
        description="Type to get suggestions",
        questions=[
            TokenBar(name="flags", options=flags, classes=["app-flags-selector"]),
            DetailComponent(title="Specify why you're changing this case's flags (optional)",
                            components=[
                                TextArea(
                                    name="note",
                                    optional=True,
                                    classes=["govuk-!-margin-0"]
                                ),
                            ]),

        ],
        default_button_name="Set flags",
        back_link=None,
        container="case",
    )
