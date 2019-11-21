from lite_content.lite_internal_frontend import strings
from lite_forms.components import Form, RadioButtonsImage, Option


def select_template_form(templates):
    options = [
        Option(t["id"], t["name"], img_url=f"/assets/images/letter_templates/{t['layout']['filename']}.png")
        for t in templates
    ]
    return Form(
        title=strings.LETTER_TEMPLATES.LetterTemplatesPage.PickTemplate.title,
        questions=[RadioButtonsImage(name="template", options=options,)],
        default_button_name=strings.LETTER_TEMPLATES.LetterTemplatesPage.PickTemplate.button,
    )
