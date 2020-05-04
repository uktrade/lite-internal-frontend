from datetime import date
from http import HTTPStatus
from typing import Dict, List

from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from cases.constants import CaseType
from cases.forms.advice import give_advice_form
from cases.forms.finalise_case import approve_licence_form, deny_licence_form
from cases.services import (
    post_user_case_advice,
    get_final_case_advice,
    coalesce_user_advice,
    coalesce_team_advice,
    post_team_case_advice,
    post_final_case_advice,
    clear_team_advice,
    clear_final_advice,
    get_case,
    finalise_application,
    post_good_countries_decisions,
    get_good_countries_decisions,
    _generate_data_and_keys,
    _generate_post_data_and_errors,
    get_application_default_duration,
    grant_licence,
    get_final_decision_documents,
    get_licence,
    get_finalise_application_goods,
)
from conf.constants import DECISIONS_LIST, Permission
from core import helpers
from core.services import get_denial_reasons
from lite_content.lite_internal_frontend.cases import GenerateFinalDecisionDocumentsPage, FinaliseLicenceForm
from lite_forms.generators import form_page, error_page
from lite_forms.views import SingleFormView


def get_goods(request, case):
    selected_goods_ids = request.GET.getlist("goods")
    goods = case.data.get("goods", case.data.get("goods_types"))
    return_values = []

    for good in goods:
        if good["id"] in selected_goods_ids:
            return_values.append(good)

    return return_values


def get_destinations(request, case):
    selected_destinations_ids = [*request.GET.getlist("destinations"), *request.GET.getlist("countries")]
    destinations = case.destinations
    return_values = []

    for destination in destinations:
        if destination["id"] in selected_destinations_ids:
            return_values.append(destination)

    return return_values


def flatten_advice_data(request, items: List[Dict]):
    if not items or not items[0].get("advice"):
        return

    first_item_advice = items[0]["advice"][0]
    keys = ["proviso", "denial_reasons", "note", "text", "type"]

    for item in items:
        for advice in [
            advice for advice in item.get("advice", []) if advice["user"]["id"] == request.user.lite_api_user_id
        ]:
            for key in keys:
                if advice[key] != first_item_advice[key]:
                    return

    return first_item_advice


class GiveAdvice(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.tab = kwargs["tab"]
        self.data = flatten_advice_data(request, [*get_goods(request, case), *get_destinations(request, case)])
        self.form = give_advice_form(
            request, case, self.tab, kwargs["queue_pk"], get_denial_reasons(request, True), show_warning=not self.data
        )
        self.context = {
            "case": case,
            "goods": get_goods(request, case),
            "destinations": get_destinations(request, case),
        }
        self.success_url = reverse(
            "cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk, "tab": self.tab}
        )

        if self.tab not in ["user-advice", "team-advice", "final-advice"]:
            raise Http404

    def get_action(self):
        if self.tab == "user-advice":
            return post_user_case_advice
        elif self.tab == "team-advice":
            return post_team_case_advice
        elif self.tab == "final-advice":
            return post_final_case_advice


class CoalesceUserAdvice(TemplateView):
    """
    Group all of a user's team's user level advice in a team advie for the user's team
    """

    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        coalesce_user_advice(request, case_id)
        return redirect(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case_id, "tab": "team-advice"})
        )


class ViewTeamAdvice(TemplateView):
    """
    View the user's team's team level advice or another team's, edit and clear the user's team's team level advice
    """

    def post(self, request, **kwargs):
        case = get_case(request, kwargs["pk"])

        if request.POST.get("action") == "delete":
            clear_team_advice(request, case.get("id"))

            return redirect(
                reverse("cases:team_advice_view", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.case.get("id")})
            )


class CoalesceTeamAdvice(TemplateView):
    """
    Group all team's advice into final advice
    """

    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        coalesce_team_advice(request, case_id)
        return redirect(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"], "tab": "final-advice"})
        )


class ViewFinalAdvice(TemplateView):
    """
    View, clear and edit final advice
    """

    def post(self, request, **kwargs):
        case = get_case(request, kwargs["pk"])

        if request.POST.get("action") == "delete":
            clear_final_advice(request, case.get("id"))

        return redirect(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"], "tab": "final-advice"})
        )


class FinaliseGoodsCountries(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            case, data, _ = _generate_data_and_keys(request, str(kwargs["pk"]))
        except PermissionError:
            return error_page(request, "You do not have permission.")

        context = {
            "title": "Finalise goods and countries",
            "case": case,
            "good_countries": data["data"],
            "decisions": DECISIONS_LIST,
        }
        return render(request, "case/views/finalise-open-goods-countries.html", context)

    def post(self, request, *args, **kwargs):
        try:
            case, data, keys = _generate_data_and_keys(request, str(kwargs["pk"]))
        except PermissionError:
            return error_page(request, "You do not have permission.")

        request_data = request.POST.copy()
        request_data.pop("csrfmiddlewaretoken")
        selection = {}
        action = request_data.pop("action")[0]

        selection["good_countries"] = []
        for key, value in request_data.items():
            selection["good_countries"].append(
                {"case": str(kwargs["pk"]), "good": key.split(".")[0], "country": key.split(".")[1], "decision": value}
            )

        context = {
            "title": "Finalise goods and countries",
            "case": case,
            "decisions": DECISIONS_LIST,
            "good_countries": data["data"],
            "errors": {},
        }

        post_data, errors = _generate_post_data_and_errors(keys, request_data, action)

        # If errors, return page
        if errors:
            context["errors"] = errors
            context["good_countries"] = post_data
            return render(request, "case/views/finalise-open-goods-countries.html", context)

        data, _ = post_good_countries_decisions(request, str(kwargs["pk"]), selection)

        if action == "save":
            context["good_countries"] = data["data"]
            return render(request, "case/views/finalise-open-goods-countries.html", context)
        elif "errors" in data:
            context["error"] = data.get("errors")
            return render(request, "case/views/finalise-open-goods-countries.html", context)

        return redirect(reverse_lazy("cases:finalise", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"]}))


class Finalise(TemplateView):
    """
    Finalise a case and change the case status to finalised
    """

    @staticmethod
    def _get_goods(request, pk, case_type):
        goods = []
        if case_type == CaseType.STANDARD.value:
            goods, status_code = get_finalise_application_goods(request, pk)
            if status_code != HTTPStatus.OK:
                return error_page(request, FinaliseLicenceForm.GOODS_ERROR)
            goods = goods["goods"]
        return goods

    def get(self, request, *args, **kwargs):
        case = get_case(request, str(kwargs["pk"]))
        case_type = case["application"]["case_type"]["sub_type"]["key"]

        if case_type == CaseType.OPEN.value:
            data = get_good_countries_decisions(request, str(kwargs["pk"]))["data"]
            items = [item["decision"]["key"] for item in data]
            is_open_licence = True
        else:
            advice, _ = get_final_case_advice(request, str(kwargs["pk"]))
            items = [item["type"]["key"] for item in advice["advice"]]
            is_open_licence = False

        case_id = case["id"]
        duration = get_application_default_duration(request, str(kwargs["pk"]))

        if "approve" in items or "proviso" in items:
            # Redirect if licence already exists
            _, status_code = get_licence(request, str(kwargs["pk"]))
            if status_code == HTTPStatus.OK:
                return redirect(
                    reverse_lazy(
                        "cases:finalise_documents", kwargs={"queue_pk": kwargs["queue_pk"], "pk": str(kwargs["pk"])}
                    )
                )

            today = date.today()
            form_data = {
                "day": today.day,
                "month": today.month,
                "year": today.year,
                "duration": duration,
            }

            form = approve_licence_form(
                queue_pk=kwargs["queue_pk"],
                case_id=case_id,
                is_open_licence=is_open_licence,
                duration=duration,
                editable_duration=helpers.has_permission(request, Permission.MANAGE_LICENCE_DURATION),
                goods=self._get_goods(request, str(kwargs["pk"]), case_type),
            )
            return form_page(request, form, data=form_data)
        else:
            return form_page(request, deny_licence_form(kwargs["queue_pk"], case_id, is_open_licence))

    def post(self, request, *args, **kwargs):
        case = get_case(request, str(kwargs["pk"]))
        is_open_licence = case["application"]["case_type"]["sub_type"]["key"] == CaseType.OPEN.value
        application_id = case.get("application").get("id")
        data = request.POST.copy()

        has_permission = helpers.has_permission(request, Permission.MANAGE_LICENCE_DURATION)

        res = finalise_application(request, application_id, data)

        if res.status_code == HTTPStatus.FORBIDDEN:
            return error_page(request, "You do not have permission.")

        if res.status_code == HTTPStatus.BAD_REQUEST:
            case_type = case["application"]["case_type"]["sub_type"]["key"]
            form = approve_licence_form(
                queue_pk=kwargs["queue_pk"],
                case_id=case["id"],
                is_open_licence=is_open_licence,
                duration=data.get("licence_duration") or get_application_default_duration(request, str(kwargs["pk"])),
                editable_duration=has_permission,
                goods=self._get_goods(request, str(kwargs["pk"]), case_type),
            )
            return form_page(request, form, data=data, errors=res.json()["errors"])

        return redirect(
            reverse_lazy("cases:finalise_documents", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case["id"]})
        )


class FinaliseGenerateDocuments(TemplateView):
    @staticmethod
    def get_page(request, pk, errors=None):
        decisions, _ = get_final_decision_documents(request, str(pk))
        decisions = decisions["documents"]
        can_submit = all([decision.get("document") for decision in decisions.values()])

        context = {
            "case_id": str(pk),
            "title": GenerateFinalDecisionDocumentsPage.TITLE,
            "can_submit": can_submit,
            "decisions": decisions,
            "errors": errors,
        }
        return render(request, "case/views/finalise-generate-documents.html", context)

    def get(self, request, pk, **kwargs):
        return self.get_page(request, pk)

    def post(self, request, pk, **kwargs):
        data, status_code = grant_licence(request, str(pk))
        if status_code != HTTPStatus.CREATED:
            return self.get_page(request, pk, errors=data["errors"])
        else:
            return redirect(reverse_lazy("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": pk}))
