from http import HTTPStatus

from django.contrib import messages
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler, s3_client

from cases.constants import CaseType
from cases.forms.Rerun_routing_rules import rerun_routing_rules_confirmation_form
from cases.forms.additional_contacts import add_additional_contact_form
from cases.forms.assign_users import assign_case_officer_form, assign_user_and_work_queue, users_team_queues
from cases.forms.attach_documents import attach_documents_form
from cases.forms.change_status import change_status_form
from cases.forms.done_with_case import done_with_case_form
from cases.forms.flags import set_case_flags_form
from cases.forms.move_case import move_case_form
from cases.objects import Slice
from cases.services import (
    get_case,
    post_case_notes,
    put_application_status,
    get_activity,
    put_case_queues,
    put_end_user_advisory_query,
    _get_total_goods_value,
    put_goods_query_status,
    get_case_officer,
    put_case_officer,
    delete_case_officer,
    put_unassign_queues,
    get_user_case_queues,
    get_case_additional_contacts,
    post_case_additional_contacts,
    put_rerun_case_routing_rules, put_flag_assignments,
)
from cases.services import post_case_documents, get_case_documents, get_document
from cases.views.ecju import get_ecju_queries
from conf import settings
from conf.constants import GENERATED_DOCUMENT, Statuses
from conf.settings import AWS_STORAGE_BUCKET_NAME
from core.builtins.custom_tags import friendly_boolean
from core.objects import Tab
from core.services import get_status_properties, get_user_permissions, get_permissible_statuses
from flags.services import get_cases_flags
from lite_content.lite_exporter_frontend import applications
from lite_content.lite_internal_frontend import cases
from lite_content.lite_internal_frontend.cases import CasePage
from lite_forms.components import Option
from lite_forms.generators import error_page, form_page
from lite_forms.views import SingleFormView
from queues.services import put_queue_single_case_assignment, get_queue
from users.services import get_gov_user_from_form_selection


def get_additional_information(case):
    """
    Returns an additional information component to be rendered by templates.
    """
    field_titles = {
        "electronic_warfare_requirement": applications.AdditionalInformation.ELECTRONIC_WARFARE_REQUIREMENT,
        "expedited": applications.AdditionalInformation.EXPEDITED,
        "expedited_date": applications.AdditionalInformation.EXPEDITED_DATE,
        "foreign_technology": applications.AdditionalInformation.FOREIGN_TECHNOLOGY,
        "foreign_technology_type": applications.AdditionalInformation.FOREIGN_TECHNOLOGY_TYPE,
        "locally_manufactured": applications.AdditionalInformation.LOCALLY_MANUFACTURED,
        "mtcr_type": applications.AdditionalInformation.MTCR_TYPE,
        "uk_service_equipment": applications.AdditionalInformation.UK_SERVICE_EQUIPMENT,
        "uk_service_equipment_type": applications.AdditionalInformation.UK_SERVICE_EQUIPMENT_TYPE,
        "value": applications.AdditionalInformation.VALUE,
    }

    values_to_print = []

    for field, title in field_titles.items():
        value = case.get(field)
        if value is not None:
            values_to_print.append(
                {
                    "Number": len(values_to_print) + 1,
                    "Description": title,
                    "Answer": (
                        friendly_boolean(value)
                        if isinstance(value, bool)
                        else value["value"]
                        if isinstance(value, dict)
                        else value
                    ),
                    "SubAnswer": case.get(f"{field}_description") if case.get(field) is True else None,
                }
            )

    return values_to_print


class ViewCase(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        case = get_case(request, case_id)
        case_type = case["case_type"]["type"]["key"]
        case_sub_type = case["case_type"]["sub_type"]["key"]
        export_type = None  # case.get("application", {}).get("export_type", {}).get("key")
        user_assigned_queues, _ = get_user_case_queues(request, case_id)
        queue_id = kwargs["queue_pk"]
        queue = get_queue(request, queue_id)
        is_system_queue = queue["is_system_queue"]

        if "application" in case:
            status_props, _ = get_status_properties(request, case["application"]["status"]["key"])
            can_set_done = (
                not status_props["is_terminal"] and case["application"]["status"]["key"] != Statuses.APPLICANT_EDITING
            )
        else:
            status_props, _ = get_status_properties(request, case["query"]["status"]["key"])
            can_set_done = (
                not status_props["is_terminal"] and case["query"]["status"]["key"] != Statuses.APPLICANT_EDITING
            )

        can_set_done = can_set_done and (is_system_queue and user_assigned_queues) or not is_system_queue

        tabs = [Tab("details", CasePage.Tabs.DETAILS, "details")]
        details = [Slice(None, "summary")]

        if case_type == CaseType.APPLICATION.value:
            tabs += [
                Tab("advice", CasePage.Tabs.ADVICE_AND_DECISION, "give-advice"),
            ]

            if case_sub_type == CaseType.OPEN.value:
                details += [Slice("Goods", "goods"),
                            Slice("Destinations", "destinations"),
                            Slice("End use details", "end-use-details"),
                            Slice("Route of goods", "route-of-goods"),
                            Slice("Supporting documents", "supporting-documents")]
                if export_type == "temporary":
                    details.insert(3, Slice("Export details", "export-details"))
            elif case_sub_type == CaseType.STANDARD.value:
                details += [Slice("Goods", "goods"),
                            Slice("Destinations", "destinations"),
                            Slice("End use details", "end-use-details"),
                            Slice("Route of goods", "route-of-goods"),
                            Slice("Supporting documents", "supporting-documents")]
            elif case_sub_type == CaseType.HMRC.value:
                details += [Slice("Goods", "goods"),
                            Slice("Destinations", "destinations"),
                            Slice("Supporting documents", "supporting-documents"),
                            Slice("hmrc deets", "hmrc")]

        if case_sub_type == CaseType.GOODS.value:
            if case.data["clc_responded"] or case.data["pv_grading_responded"]:
                details += [Slice(None, "goods-query-response")]

            details += [Slice("Query details", "goods-query")]

        if case_sub_type == CaseType.END_USER_ADVISORY.value:
            details += [Slice("End user details", "end-user-advisory")]

        tabs += [
            Tab("documents", CasePage.Tabs.DOCUMENTS, "documents"),
            Tab("additional-contacts", CasePage.Tabs.ADDITIONAL_CONTACTS, "additional-contacts"),
            Tab("ecju-queries", CasePage.Tabs.ECJU_QUERIES, "ecju-queries"),
            Tab("activity", CasePage.Tabs.CASE_NOTES_AND_TIMELINE, "activity"),
        ]

        case_documents, _ = get_case_documents(request, case_id)
        open_ecju_queries, closed_ecju_queries = get_ecju_queries(request, case_id)

        context = {
            "tabs": tabs,
            "current_tab": kwargs["tab"],
            "details": details,
            "activity": get_activity(request, case_id),
            "case": case,
            "queue": queue,
            "permissions": get_user_permissions(request),
            "permissible_statuses": get_permissible_statuses(request, case_type),
            "status_is_read_only": status_props["is_read_only"],
            "status_is_terminal": status_props["is_terminal"],
            "can_set_done": can_set_done,
            "case_documents": case_documents["documents"],
            "generated_document_key": GENERATED_DOCUMENT,
            "additional_contacts": get_case_additional_contacts(request, case_id),
            "open_ecju_queries": open_ecju_queries,
            "closed_ecju_queries": closed_ecju_queries,
        }

        return render(request, "case/case.html", context)

    def post(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        response, status_code = post_case_notes(request, case_id, request.POST)

        if status_code != 201:

            errors = response.get("errors")
            if errors.get("text"):
                error = errors.get("text")[0]
                error = error.replace("This field", "Case note")
                error = error.replace("this field", "the case note")  # TODO: Move to API

            else:
                error_list = []
                for key in errors:
                    error_list.append("{field}: {error}".format(field=key, error=errors[key][0]))
                error = "\n".join(error_list)
            return error_page(request, error)

        return redirect(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case_id, "tab": "activity"})
        )


class CaseImDoneView(TemplateView):
    case_pk = None
    queue_pk = None
    is_system_queue = None

    def dispatch(self, request, *args, **kwargs):
        self.case_pk = kwargs["pk"]
        self.queue_pk = kwargs["queue_pk"]
        queue = get_queue(request, self.queue_pk)
        self.is_system_queue = queue["is_system_queue"]

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        if self.is_system_queue:
            return form_page(request, done_with_case_form(request, self.case_pk))
        else:
            data, status_code = put_unassign_queues(request, self.case_pk, {"queues": [str(self.queue_pk)]})
            if status_code != HTTPStatus.OK:
                return error_page(request, description=data["errors"]["queues"][0],)
            return redirect(reverse_lazy("queues:cases", kwargs={"queue_pk": self.queue_pk}))

    def post(self, request, **kwargs):
        data, status_code = put_unassign_queues(request, self.case_pk, {"queues": request.POST.getlist("queues[]")})

        if status_code != HTTPStatus.OK:
            return error_page(request, description=data["errors"]["queues"][0],)

        return redirect(reverse_lazy("queues:cases", kwargs={"queue_pk": self.queue_pk}))


class ViewAdvice(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        case = get_case(request, case_id)
        activity, _ = get_activity(request, case_id)
        permissions = get_user_permissions(request)

        context = {
            "data": case,
            "activity": activity.get("activity"),
            "permissions": permissions,
            "edit_case_flags": cases.Case.EDIT_CASE_FLAGS,
        }
        return render(request, "case/advice/user.html", context)


class ChangeStatus(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        case = get_case(request, self.object_pk)
        self.case_type = case["case_type"]["type"]["key"]
        self.case_sub_type = case["case_type"]["sub_type"]["key"]
        permissible_statuses = get_permissible_statuses(request, self.case_type)
        self.data = case["application"] if "application" in case else case["query"]
        self.form = change_status_form(get_queue(request, kwargs["queue_pk"]), case, permissible_statuses)
        self.context = {"case": case}

    def get_action(self):
        if (
            self.case_type == CaseType.APPLICATION.value
            or self.case_sub_type == CaseType.HMRC.value
            or self.case_sub_type == CaseType.EXHIBITION.value
        ):
            return put_application_status
        elif self.case_sub_type == CaseType.END_USER_ADVISORY.value:
            return put_end_user_advisory_query
        elif self.case_sub_type == CaseType.GOODS.value:
            return put_goods_query_status

    def get_success_url(self):
        messages.success(self.request, cases.ChangeStatusPage.SUCCESS_MESSAGE)
        return reverse_lazy("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk})


class MoveCase(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.data = case
        self.form = move_case_form(request, get_queue(request, kwargs["queue_pk"]), case)
        self.action = put_case_queues
        self.context = {"case": case}
        self.success_message = cases.Manage.MoveCase.SUCCESS_MESSAGE
        self.success_url = reverse_lazy("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk})


class AddAnAdditionalContact(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = add_additional_contact_form(request, self.kwargs["queue_pk"], self.object_pk)
        self.action = post_case_additional_contacts
        self.success_message = cases.CasePage.AdditionalContactsTab.SUCCESS_MESSAGE
        self.context = {"case": get_case(request, self.object_pk)}
        self.success_url = reverse(
            "cases:case",
            kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk, "tab": "additional-contacts"},
        )


@method_decorator(csrf_exempt, "dispatch")
class AttachDocuments(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        case = get_case(request, case_id)

        form = attach_documents_form(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case_id, "tab": "documents"})
        )

        return form_page(request, form, extra_data={"case_id": case_id, "case": case})

    @csrf_exempt
    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        case_id = str(kwargs["pk"])
        data = []

        files = request.FILES.getlist("file")
        if len(files) != 1:
            return error_page(None, "We had an issue uploading your files. Try again later.")
        file = files[0]
        data.append(
            {
                "name": file.original_name,
                "s3_key": file.name,
                "size": int(file.size // 1024) if file.size else 0,  # in kilobytes
                "description": request.POST["description"],
            }
        )

        # Send LITE API the file information
        case_documents, _ = post_case_documents(request, case_id, data)

        if "errors" in case_documents:
            return error_page(None, "We had an issue uploading your files. Try again later.")

        return redirect(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case_id, "tab": "documents"})
        )


class Document(TemplateView):
    def get(self, request, **kwargs):
        file_pk = str(kwargs["file_pk"])

        document, _ = get_document(request, file_pk)
        original_file_name = document["document"]["name"]

        # Stream file
        def generate_file(result):
            for chunk in iter(lambda: result["Body"].read(settings.STREAMING_CHUNK_SIZE), b""):
                yield chunk

        s3 = s3_client()
        s3_key = document["document"]["s3_key"]
        s3_response = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_key)
        _kwargs = {}
        if s3_response.get("ContentType"):
            _kwargs["content_type"] = s3_response["ContentType"]
        response = StreamingHttpResponse(generate_file(s3_response), **_kwargs)
        response["Content-Disposition"] = f'attachment; filename="{original_file_name}"'
        return response


class CaseOfficer(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.data = {"gov_user_pk": case.case_officer.get("id")}
        self.form = assign_case_officer_form(request, case.case_officer)
        self.context = {"case": case}
        self.success_url = reverse("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk})

    def get_action(self):
        action = self.get_validated_data().get("_action")

        if action == "delete":
            self.success_message = "Case officer removed"
            return delete_case_officer
        else:
            self.success_message = "Case officer set successfully"
            return put_case_officer


class UserWorkQueue(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.form = assign_user_and_work_queue(request)
        self.action = get_gov_user_from_form_selection
        self.context = {"case": case}

    def get_success_url(self):
        user_id = self.get_validated_data().get("user").get("id")
        return reverse_lazy(
            "cases:assign_user_queue",
            kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk, "user_pk": user_id},
        )


class UserTeamQueue(SingleFormView):
    def init(self, request, **kwargs):
        user_pk = str(kwargs["user_pk"])
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.form = users_team_queues(request, str(kwargs["pk"]), user_pk)
        self.action = put_queue_single_case_assignment
        self.context = {"case": case}

    def get_success_url(self):
        return reverse_lazy("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk})


class RerunRoutingRules(SingleFormView):
    def init(self, request, **kwargs):
        self.action = put_rerun_case_routing_rules
        self.object_pk = kwargs["pk"]
        self.form = rerun_routing_rules_confirmation_form()
        self.success_url = reverse_lazy(
            "cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk}
        )

    def post(self, request, **kwargs):
        self.init(request, **kwargs)
        if not request.POST.get("confirm"):
            return form_page(
                request,
                self.get_form(),
                data=self.get_data(),
                errors={"confirm": ["select an option"]},
                extra_data=self.context,
            )
        elif request.POST.get("confirm") == "no":
            return redirect(self.success_url)

        return super(RerunRoutingRules, self).post(request, **kwargs)


def perform_action(request, pk, json):
    data = {
        "level": "cases",
        "objects": [str(pk)],
        "flags": json.get("flags", []),
        "note": json.get("note"),
    }
    return put_flag_assignments(request, data)


class AssignFlags(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        flags = [flag for flag in get_cases_flags(request) if flag not in case["flags"]]
        self.data = {"flags": [Option(flag["id"],
                                      flag["name"],
                                      classes=["app-flag", "app-flag--" + flag["colour"]]) for flag in case["flags"]]}
        self.form = set_case_flags_form(kwargs["queue_pk"], flags, case)
        self.context = {"case": case, "hide_flags_row": True}
        self.action = perform_action
        self.success_url = reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk})
