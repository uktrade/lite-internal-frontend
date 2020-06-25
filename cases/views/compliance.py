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
    delete_compliance_person_present,
    get_compliance_person_present,
    patch_compliance_person_present,
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
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": new_case_id, "tab": "activity"})
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


class AddPeoplePresent(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = people_present_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.action = post_compliance_person_present

    def on_submission(self, request, **kwargs):
        data = request.POST.copy()
        data["visit_case"] = str(kwargs["pk"])
        return data


class EditPeoplePresent(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["person_id"]
        self.form = people_present_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"]})
        self.data = get_compliance_person_present(request, kwargs["person_id"])
        self.action = patch_compliance_person_present


class RemovePeoplePresent(TemplateView):
    def get(self, request, *args, **kwargs):

        delete_compliance_person_present(request, kwargs["person_id"])

        return redirect(reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"]}))


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
