from django.urls import reverse_lazy

from lite_content.lite_internal_frontend.cases import GenerateDocumentsPage
from lite_content.lite_internal_frontend.strings import letter_templates
from lite_forms.components import Form, RadioButtonsImage, Option, BackLink, TextArea, Custom


def select_template_form(templates, back_url):
    return Form(
        title=letter_templates.LetterTemplatesPage.PickTemplate.TITLE,
        questions=[
            RadioButtonsImage(
                name="template",
                options=[
                    Option(t["id"], t["name"], img_url=f"/assets/images/letter_templates/{t['layout']['filename']}.png")
                    for t in templates["results"]
                ],
                total_pages=templates,
            )
        ],
        default_button_name=letter_templates.LetterTemplatesPage.PickTemplate.BUTTON,
        back_link=BackLink(url=back_url),
        container="case",
    )


def select_addressee_form(back_url):
    return Form("Select Addressee", questions=[Custom("components/addressee-table.html")], back_link=BackLink(url=back_url), container="case",)


def edit_document_text_form(kwargs, post_url, back_url):
    return Form(
        title=GenerateDocumentsPage.EditTextForm.HEADING,
        questions=[TextArea(name="text", extras={"max_length": 5000}),],
        default_button_name=GenerateDocumentsPage.EditTextForm.BUTTON,
        post_url=reverse_lazy(post_url, kwargs=kwargs),
        back_link=BackLink(url=back_url),
        container="case",
    )
