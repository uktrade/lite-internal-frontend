from django.urls import reverse_lazy

from lite_content.lite_internal_frontend import strings
from lite_content.lite_internal_frontend.cases import GenerateDocumentsPage
from lite_forms.components import Form, RadioButtonsImage, Option, BackLink, TextArea, Link


def select_template_form(templates, case_id):
    return Form(
        title=strings.LETTER_TEMPLATES.LetterTemplatesPage.PickTemplate.title,
        questions=[
            RadioButtonsImage(
                name="template",
                options=[
                    Option(t["id"], t["name"], img_url=f"/assets/images/letter_templates/{t['layout']['filename']}.png")
                    for t in templates
                ],
            )
        ],
        default_button_name=strings.LETTER_TEMPLATES.LetterTemplatesPage.PickTemplate.button,
        back_link=BackLink(
            text=GenerateDocumentsPage.SelectTemplateForm.BACK_LINK,
            url=reverse_lazy("cases:case", kwargs={"pk": case_id}),
        ),
    )


def edit_document_text_form(case_id, kwargs):
    return Form(
        title="Edit text",
        questions=[
            TextArea(title="Text", name="text", extras={"max_length": 5000}),
            Link(name="add_paragraphs", url=reverse_lazy("cases:generate_document_add_paragraphs"), text="Add paragraphs")
        ],
        default_button_name="Continue",
        back_link=BackLink(text="Back", url=reverse_lazy("cases:generate_document", kwargs={"pk": case_id})),
        post_url=reverse_lazy("cases:generate_document_preview", kwargs=kwargs)
    )
