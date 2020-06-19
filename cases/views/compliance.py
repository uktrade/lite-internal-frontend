from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from cases.services import post_create_compliance_visit


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
