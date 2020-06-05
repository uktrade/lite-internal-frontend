from django.shortcuts import render
from django.views.generic import TemplateView

from core.helpers import convert_dict_to_query_params
from letter_templates.services import (
    get_letter_templates,
    get_letter_template,
)
from lite_forms.components import FiltersBar, TextInput


class LetterTemplatesList(TemplateView):
    def get(self, request, **kwargs):
        params = {"page": int(request.GET.get("page", 1))}
        name = request.GET.get("name")
        if name:
            params["name"] = name

        data, _ = get_letter_templates(request, convert_dict_to_query_params(params))
        filters = FiltersBar(
            [TextInput(name="name", title="name"), ]
        )
        context = {"data": data, "page": params.pop("page"), "filters": filters,}
        return render(request, "letter-templates/letter-templates.html", context)


class LetterTemplateDetail(TemplateView):
    def get(self, request, **kwargs):
        letter_template_id = str(kwargs["pk"])
        params = convert_dict_to_query_params({"generate_preview": True, "activity": True})
        response, _ = get_letter_template(request, letter_template_id, params=params)
        context = {
            "letter_template": response["template"],
            "preview": response["preview"],
            "activity": response.get("activity", []),
        }
        return render(request, "letter-templates/letter-template.html", context)
