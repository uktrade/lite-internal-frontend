from django.shortcuts import render
from django.views.generic import TemplateView

from letter_templates import helpers
from letter_templates.helpers import paragraphs_to_markdown
from letter_templates.services import (
    get_letter_paragraphs,
    get_letter_templates,
    get_letter_template,
    get_template_preview)


class LetterTemplatesList(TemplateView):
    def get(self, request, **kwargs):
        context = {"letter_templates": get_letter_templates(request)}
        return render(request, "letter_templates/letter_templates.html", context)


class LetterTemplateDetail(TemplateView):
    def get(self, request, **kwargs):
        letter_template_id = str(kwargs["pk"])
        letter_template = get_letter_template(request, letter_template_id)
        preview = get_template_preview(request, letter_template_id)[0]["preview"]
        context = {
            "letter_template": letter_template,
            "preview": preview,
        }
        return render(request, "letter_templates/letter_template.html", context)
