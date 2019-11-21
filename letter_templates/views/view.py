from django.shortcuts import render
from django.views.generic import TemplateView

from letter_templates.services import (
    get_letter_templates,
    get_letter_template)


class LetterTemplatesList(TemplateView):
    def get(self, request, **kwargs):
        context = {"letter_templates": get_letter_templates(request)}
        return render(request, "letter_templates/letter_templates.html", context)


class LetterTemplateDetail(TemplateView):
    def get(self, request, **kwargs):
        letter_template_id = str(kwargs["pk"])
        template = get_letter_template(request, letter_template_id, generate_preview=True)[0]
        context = {
            "letter_template": template["template"],
            "preview": template["preview"],
        }
        return render(request, "letter_templates/letter_template.html", context)
