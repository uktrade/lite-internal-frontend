from cases.helpers import case_view_breadcrumbs
from lite_forms.components import Form, Filter, Checkboxes, TextArea, BackLink


def flags_form(flags, level, origin, url):

    if level == "cases":
        title = "Edit case flags"
        back_link = case_view_breadcrumbs({'name': 'asd'}, title)
    else:
        title = f"Set {level} flags"
        back_link = BackLink("Back to " + origin, url)

    return Form(
        title=title,
        description="Select all flags that apply",
        questions=[
            Filter(placeholder="Filter flags"),
            Checkboxes(name="flags", options=flags),
            TextArea(
                name="note",
                title="Notes",
                description="Provide reasons for editing the flags on these " + level,
                optional=True,
            ),
        ],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        back_link=back_link,
    )
