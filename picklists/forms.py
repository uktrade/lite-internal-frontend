from lite_content.lite_internal_frontend import strings
from django.urls import reverse_lazy
from lite_forms.components import TextInput, TextArea, Form, Button, MarkdownArea, HiddenField, BackLink, HelpSection
from lite_forms.helpers import conditional
from lite_forms.styles import ButtonStyle

from letter_templates.context_variables import get_sample_context_variables


def add_picklist_item_form(request):
    picklist_type = request.GET.get("type")

    return Form(
        title=getattr(strings.Picklist.Create, picklist_type.upper()),
        questions=[
            TextInput(title="Name", name="name"),
            HiddenField("type", picklist_type),
            TextArea(title="Text", name="text", extras={"max_length": 5000,}),
        ],
        back_link=BackLink("Back to picklists", reverse_lazy("picklists:picklists") + f"?type={picklist_type}"),
        default_button_name="Save",
    )


def edit_picklist_item_form(picklist_item):
    deactivate_button = Button(
        value="Deactivate",
        action="",
        style=ButtonStyle.WARNING,
        link=reverse_lazy("picklists:deactivate", kwargs={"pk": picklist_item["id"]}),
        float_right=True,
    )
    activate_button = Button(
        value="Reactivate",
        action="",
        style=ButtonStyle.SECONDARY,
        link=reverse_lazy("picklists:reactivate", kwargs={"pk": picklist_item["id"]}),
        float_right=True,
    )

    return Form(
        title="Edit " + picklist_item["name"],
        questions=[
            TextInput(title="Name", name="name"),
            HiddenField("type", picklist_item["type"]["key"]),
            TextArea(title="Text", name="text", extras={"max_length": 5000,}),
        ],
        back_link=BackLink(
            "Back to " + picklist_item["name"],
            reverse_lazy("picklists:picklist_item", kwargs={"pk": picklist_item["id"]}),
        ),
        buttons=[
            Button("Save", "submit", ButtonStyle.DEFAULT),
            conditional(picklist_item["status"]["key"] == "deactivated", activate_button, deactivate_button),
        ],
    )


def add_letter_paragraph_form(picklist_type):
    return Form(
        title="Create a letter paragraph",
        description="",
        questions=[
            HiddenField("type", picklist_type),
            TextInput(title="Name", name="name", classes=["govuk-!-width-full"]),
            MarkdownArea(
                title="Paragraph Text",
                name="text",
                variables=get_sample_context_variables(),
                extras={"max_length": 5000,},
            ),
        ],
        helpers=[HelpSection("Help", None, "teams/markdown-help.html")],
    )


def edit_letter_paragraph_form(picklist_item):
    return Form(
        title="Edit " + picklist_item["name"],
        description="",
        questions=[
            HiddenField("type", picklist_item["type"]["key"]),
            TextInput(title="Name", name="name", classes=["govuk-!-width-full"]),
            MarkdownArea(
                title="Paragraph Text",
                name="text",
                variables=get_sample_context_variables(),
                extras={"max_length": 5000,},
            ),
        ],
        helpers=[HelpSection("Help", None, "teams/markdown-help.html")],
    )


def deactivate_picklist_item(picklist_item):
    return Form(
        title="Are you sure you want to deactivate " + picklist_item["name"] + "?",
        description="You can always reactivate it later if need be.",
        questions=[],
        back_link=BackLink("Back", reverse_lazy("picklists:edit", kwargs={"pk": picklist_item["id"]})),
        buttons=[
            Button("Deactivate", "submit", ButtonStyle.WARNING),
            Button(
                "Cancel",
                "cancel",
                ButtonStyle.SECONDARY,
                reverse_lazy("picklists:edit", kwargs={"pk": picklist_item["id"]}),
            ),
        ],
    )


def reactivate_picklist_item(picklist_item):
    return Form(
        title="Are you sure you want to reactivate " + picklist_item["name"] + "?",
        description="You can always deactivate it later if need be.",
        questions=[],
        back_link=BackLink("Back", reverse_lazy("picklists:edit", kwargs={"pk": picklist_item["id"]})),
        buttons=[
            Button("Reactivate", "submit", ButtonStyle.DEFAULT),
            Button(
                "Cancel",
                "cancel",
                ButtonStyle.SECONDARY,
                reverse_lazy("picklists:edit", kwargs={"pk": picklist_item["id"]}),
            ),
        ],
    )
