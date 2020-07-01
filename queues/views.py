from http import HTTPStatus

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from cases.forms.assign_users import assign_users_form
from cases.forms.attach_documents import upload_document_form
from cases.helpers.filters import case_filters_bar
from conf.constants import ALL_CASES_QUEUE_ID, Permission
from core.helpers import convert_parameters_to_query_params
from core.services import get_user_permissions
from lite_content.lite_internal_frontend.cases import CasesListPage, UploadEnforcementXML
from lite_forms.components import TextInput, FiltersBar
from lite_forms.generators import error_page, form_page
from lite_forms.views import SingleFormView
from queues.forms import new_queue_form, edit_queue_form
from queues.services import (
    get_queues,
    post_queues,
    get_queue,
    put_queue,
    get_queue_case_assignments,
    put_queue_case_assignments,
    get_enforcement_xml,
    post_enforcement_xml,
)
from users.services import get_gov_user


class Cases(TemplateView):
    def get(self, request, **kwargs):
        """
        Show a list of cases pertaining to the given queue
        """
        queue_pk = kwargs.get("queue_pk") or request.user.default_queue

        context = {
            "queue": get_queue(request, queue_pk),  # Used for showing current queue
            "filters": case_filters_bar(request),
            "params": convert_parameters_to_query_params(request.GET),  # Used for passing params to JS
            "is_all_cases_queue": queue_pk == ALL_CASES_QUEUE_ID,
            "enforcement_check": Permission.ENFORCEMENT_CHECK.value in get_user_permissions(request),
        }
        return render(request, "queues/cases.html", context)

    def post(self, request, **kwargs):
        """ Assign users depending on what cases were selected. """
        return redirect(
            reverse("queues:case_assignments", kwargs={"pk": kwargs["queue_pk"]})
            + "?cases="
            + ",".join(request.POST.getlist("cases"))
        )


class QueuesList(TemplateView):
    def get(self, request, **kwargs):
        page = request.GET.get("page", 1)
        name = request.GET.get("name")
        queues = get_queues(request, page=page, disable_pagination=False, name=name)
        user_data, _ = get_gov_user(request, str(request.user.lite_api_user_id))

        filters = FiltersBar([TextInput(name="name", title="name"),])

        context = {
            "data": queues,
            "user_data": user_data,
            "filters": filters,
            "name": name,
        }
        return render(request, "queues/manage.html", context)


class AddQueue(SingleFormView):
    def init(self, request, **kwargs):
        self.form = new_queue_form(request)
        self.action = post_queues
        self.success_url = reverse_lazy("queues:manage")


class EditQueue(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_queue(request, self.object_pk)
        self.form = edit_queue_form(request, self.object_pk)
        self.action = put_queue
        self.success_url = reverse_lazy("queues:manage")


class CaseAssignments(TemplateView):
    def get(self, request, **kwargs):
        """
        Assign users to cases
        """
        queue_id = str(kwargs["pk"])
        queue = get_queue(request, queue_id)
        case_assignments, _ = get_queue_case_assignments(request, queue_id)

        case_ids = request.GET.get("cases").split(",")
        user_data, _ = get_gov_user(request, str(request.user.lite_api_user_id))

        # If no cases have been selected, return an error page
        if not request.GET.get("cases"):
            return error_page(request, "Invalid case selection")

        # Get assigned users
        assigned_users = [
            assignment["user"] for assignment in case_assignments["case_assignments"] if assignment["case"] in case_ids
        ]
        return form_page(
            request,
            assign_users_form(request, user_data["user"]["team"]["id"], queue, len(case_ids) > 1),
            data={"users": assigned_users},
        )

    def post(self, request, **kwargs):
        """
        Update the queue's case assignments
        """
        queue_id = str(kwargs["pk"])
        queue = get_queue(request, queue_id)
        case_ids = request.GET.get("cases").split(",")
        user_data, _ = get_gov_user(request, str(request.user.lite_api_user_id))

        # Any assignments not selected should be removed (hence clear_existing_assignments)
        data = {"case_assignments": [], "remove_existing_assignments": True}

        # Append case and users to case assignments
        for case_id in case_ids:
            data["case_assignments"].append({"case_id": case_id, "users": request.POST.getlist("users")})

        response, _ = put_queue_case_assignments(request, queue_id, data)
        if "errors" in response:
            return form_page(
                request,
                assign_users_form(request, user_data["user"]["team"]["id"], queue, len(case_ids) > 1),
                data=request.POST,
                errors=response["errors"],
            )

        # If there is no response (no forms left to go through), go to the case page
        return redirect(reverse("queues:cases", kwargs={"queue_pk": queue_id}))


class EnforcementXMLExport(TemplateView):
    def get(self, request, pk):
        data, status_code = get_enforcement_xml(request, pk)

        if status_code == HTTPStatus.NO_CONTENT:
            return error_page(request, CasesListPage.EnforcementXML.Export.NO_CASES)
        elif status_code != HTTPStatus.OK:
            return error_page(request, CasesListPage.EnforcementXML.Export.GENERIC_ERROR)
        else:
            return data


class EnforcementXMLImport(SingleFormView):
    def init(self, request, pk):
        self.object_pk = str(pk)
        self.form = upload_document_form(self.object_pk)
        self.action = post_enforcement_xml

    def get_success_url(self):
        messages.success(self.request, UploadEnforcementXML.SUCCESS_BANNER)
        return reverse_lazy("queues:enforcement_xml_import", kwargs={"pk": self.object_pk})
