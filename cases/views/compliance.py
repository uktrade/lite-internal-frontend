from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from cases.forms.compliance import (
    visit_report_form,
    people_present_form,
    overview_form,
    inspection_form,
    compliance_with_licence_form,
    knowledge_of_people_form,
    knowledge_of_products_form,
)
from cases.services import (
    post_create_compliance_visit,
    patch_compliance_visit_case,
    get_compliance_visit_case,
    post_compliance_person_present,
    get_case,
    get_compliance_people_present,
)
from lite_forms.views import SingleFormView


class CreateVisitReport(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        response = post_create_compliance_visit(request, case_id)

        if response.status_code != 201:
            return redirect(
                reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case_id, "tab": "details"})
            )

        new_case_id = response.json()["data"]["id"]

        return redirect(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": new_case_id, "tab": "details"})
        )


class VisitReportDetails(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = visit_report_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.action = patch_compliance_visit_case
        self.data = get_compliance_visit_case(request, kwargs["pk"])

    def get_data(self):
        data = self.data
        field = "visit_date"
        if data.get(field, False):
            date_split = data[field].split("-")
            data[field + "_year"], data[field + "_month"], data[field + "_day"] = date_split
        return data


class PeoplePresent(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.context = {"case": get_case(request, self.object_pk)}
        self.data = get_compliance_people_present(request, self.object_pk)
        self.form = people_present_form(kwargs["queue_pk"], kwargs["pk"], self.data)
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.success_message = "People present updated successfully"
        self.action = post_compliance_person_present

    def on_submission(self, request, **kwargs):
        data = request.POST.copy()
        data["people_present"] = []
        i = 0

        while i < len(data.getlist("name[]")):
            data["people_present"].append(
                {"name": data.getlist("name[]")[i], "job_title": data.getlist("job_title[]")[i],}
            )
            i += 1

        data["visit_case"] = str(kwargs["pk"])
        return data


class Overview(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = overview_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.action = patch_compliance_visit_case
        self.data = get_compliance_visit_case(request, kwargs["pk"])


class Inspection(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = inspection_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.action = patch_compliance_visit_case
        self.data = get_compliance_visit_case(request, kwargs["pk"])


class ComplianceWithLicences(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = compliance_with_licence_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.action = patch_compliance_visit_case
        self.data = get_compliance_visit_case(request, kwargs["pk"])


class KnowledgePeople(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = knowledge_of_people_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.action = patch_compliance_visit_case
        self.data = get_compliance_visit_case(request, kwargs["pk"])


class KnowledgeProduct(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = knowledge_of_products_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.action = patch_compliance_visit_case
        self.data = get_compliance_visit_case(request, kwargs["pk"])
