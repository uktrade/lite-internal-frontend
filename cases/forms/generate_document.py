from django.urls import reverse_lazy

from core.helpers import convert_dict_to_query_params
from letter_templates.services import get_letter_templates
from lite_content.lite_internal_frontend.cases import GenerateDocumentsPage
from lite_content.lite_internal_frontend.strings import letter_templates
from lite_forms.components import Form, RadioButtonsImage, Option, BackLink, TextArea, Custom


def select_template_form(request, kwargs):
    page = request.GET.get("page", 1)
    params = {"case": kwargs["pk"], "page": page}
    templates, _ = get_letter_templates(request, convert_dict_to_query_params(params))

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
        back_link=BackLink(url=reverse_lazy("cases:case", kwargs=kwargs)),
        container="case",
    )


def select_addressee_form():
    return Form("Select Addressee", questions=[Custom("components/addressee-table.html")], container="case",)


def edit_document_text_form(kwargs, template_id):
    kwargs["tpk"] = template_id

    return Form(
        title=GenerateDocumentsPage.EditTextForm.HEADING,
        questions=[TextArea(name="text", extras={"max_length": 5000}),],
        default_button_name=GenerateDocumentsPage.EditTextForm.BUTTON,
        back_link=BackLink(url=reverse_lazy("cases:generate_document", kwargs=kwargs),),
        post_url=reverse_lazy("cases:generate_document_preview", kwargs=kwargs),
        container="case",
    )
