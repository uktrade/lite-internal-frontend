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
from cases.services import post_create_compliance_visit
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


class AddPeoplePresent(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = people_present_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)


class EditPeoplePresent(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = people_present_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)


class RemovePeoplePresent(TemplateView):
    pass


class Overview(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = overview_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)


class Inspection(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = inspection_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)


class ComplianceWithLicences(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = compliance_with_licence_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)


class KnowledgePeople(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = knowledge_of_people_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)


class KnowledgeProduct(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = knowledge_of_products_form(kwargs["queue_pk"], kwargs["pk"])
        self.success_url = reverse("cases:case", kwargs=kwargs)
