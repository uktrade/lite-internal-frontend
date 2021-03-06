from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from cases.services import get_case_types, get_decisions
from lite_forms.components import Option
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form

from letter_templates.forms import edit_letter_template
from letter_templates.services import (
    get_letter_template,
    put_letter_template,
    get_letter_paragraphs,
)
from picklists.services import get_picklists_for_input


class EditTemplate(TemplateView):
    def get(self, request, **kwargs):
        letter_template = get_letter_template(request, str(kwargs["pk"]))[0]["template"]
        letter_template_case_types = letter_template.pop("case_types") or []
        letter_template_decisions = letter_template.pop("decisions") or []

        letter_template_case_types = [case_type["reference"]["key"] for case_type in letter_template_case_types]
        letter_template.update(case_types=letter_template_case_types)

        letter_template_decisions = [decision["name"]["key"] for decision in letter_template_decisions]
        letter_template.update(decisions=letter_template_decisions)

        case_type_options = [Option(option["key"], option["value"]) for option in get_case_types(request)]
        decision_options = [Option(decision["key"], decision["value"]) for decision in get_decisions(request)[0]]

        return form_page(
            request,
            edit_letter_template(request, letter_template, case_type_options, decision_options),
            data=letter_template,
        )

    @staticmethod
    def post(request, **kwargs):
        letter_template_id = str(kwargs["pk"])
        letter_template = get_letter_template(request, letter_template_id)[0]["template"]

        # Override case restrictions to use getlist
        edited_letter_template_data = request.POST.copy()
        edited_letter_template_data["case_types"] = edited_letter_template_data.getlist("case_types[]")
        edited_letter_template_data["decisions"] = edited_letter_template_data.getlist("decisions[]")

        case_type_options = [Option(option["key"], option["value"]) for option in get_case_types(request)]
        decision_options = [Option(decision["key"], decision["value"]) for decision in get_decisions(request)[0]]

        next_form, _ = submit_single_form(
            request,
            edit_letter_template(request, letter_template, case_type_options, decision_options),
            put_letter_template,
            object_pk=letter_template_id,
            override_data=edited_letter_template_data,
        )

        if next_form:
            return next_form

        return redirect(reverse("letter_templates:letter_template", kwargs={"pk": letter_template_id}))


class EditParagraphs(TemplateView):
    def get(self, request, **kwargs):
        letter_template = get_letter_template(request, str(kwargs["pk"]))[0]["template"]
        letter_paragraphs = get_letter_paragraphs(request, letter_template["letter_paragraphs"])
        letter_paragraphs = self.sort_letter_paragraphs(letter_paragraphs, letter_template["letter_paragraphs"])

        context = {"letter_template": letter_template, "letter_paragraphs": letter_paragraphs}
        return render(request, "letter-templates/edit-letter-paragraphs.html", context)

    @staticmethod
    def sort_letter_paragraphs(paragraphs, ids):
        """Order a list of letter paragraphs in the same order as a list of IDs."""
        paragraphs_by_id = {p["id"]: p for p in paragraphs}
        return [paragraphs_by_id[id] for id in ids if id in paragraphs_by_id]

    @staticmethod
    def _add_letter_paragraph(request, existing_paragraphs):
        all_letter_paragraphs = get_picklists_for_input(request, "letter_paragraph")
        context = {
            "letter_paragraphs": [
                paragraph for paragraph in all_letter_paragraphs if paragraph["id"] not in existing_paragraphs
            ],
            "existing_letter_paragraphs": existing_paragraphs,
        }
        return render(request, "letter-templates/add-letter-paragraphs.html", context)

    def post(self, request, **kwargs):
        letter_template_id = str(kwargs["pk"])
        action = request.POST.get("action")
        paragraphs = request.POST.getlist("letter_paragraphs")

        if action == "add_letter_paragraph":
            return self._add_letter_paragraph(request, paragraphs)

        elif "delete" in action:
            pk_to_delete = action.split(".")[1]
            paragraphs.remove(pk_to_delete)

        put_letter_template(request, letter_template_id, {"letter_paragraphs": paragraphs})

        if "edit" in action:
            return redirect(reverse("letter_templates:letter_template", kwargs={"pk": letter_template_id}))
        else:
            return self.get(request, **kwargs)
