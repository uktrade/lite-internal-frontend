from django.urls import reverse_lazy

from letter_templates.context_variables import get_sample_context_variables
from lite_content.lite_internal_frontend import strings
from lite_content.lite_internal_frontend.cases import GenerateDocumentsPage
from lite_forms.components import (
    Form,
    RadioButtonsImage,
    Option,
    BackLink,
    SubmitButton,
    Checkboxes,
    HiddenField,
    MarkdownArea,
)

ADD_PARAGRAPH_KEY = "add_paragraphs"


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
            MarkdownArea(
                title="Text", variables=get_sample_context_variables(), name="text", extras={"max_length": 5000}
            ),
            SubmitButton(
                name=ADD_PARAGRAPH_KEY,
                text="Add paragraphs",
                formaction=reverse_lazy("cases:generate_document_add_paragraphs", kwargs=kwargs),
            ),
        ],
        default_button_name="Continue",
        back_link=BackLink(text="Back", url=reverse_lazy("cases:generate_document", kwargs={"pk": case_id})),
        post_url=reverse_lazy("cases:generate_document_preview", kwargs=kwargs),
    )


def add_paragraphs_form(paragraphs, text, kwargs):
    return Form(
        title="Add paragraphs",
        questions=[
            HiddenField(name="text[]", value=text),
            Checkboxes(
                name="text[]", options=[Option(paragraph["text"], paragraph["name"]) for paragraph in paragraphs],
            ),
        ],
        back_link=BackLink(),
        default_button_name="Continue",
        post_url=reverse_lazy("cases:generate_document_edit", kwargs=kwargs),
    )
