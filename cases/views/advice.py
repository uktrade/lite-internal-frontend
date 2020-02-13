from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from cases.constants import CaseType

from datetime import date

from cases.forms.finalise_case import approve_licence_form, deny_licence_form

from cases.services import (
    post_user_case_advice,
    get_user_case_advice,
    get_team_case_advice,
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
)
from cases.views_helpers import (
    get_case_advice,
    render_form_page,
    post_advice,
    post_advice_details,
    give_advice_detail_dispatch,
    give_advice_dispatch,
)
from conf.constants import DECISIONS_LIST, Permission
from core import helpers
from lite_forms.generators import form_page, error_page


class ViewUserAdvice(TemplateView):
    """
    View advice at a user level and select advice to edit
    """

    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form = give_advice_dispatch("user", request, **kwargs)
        return super(ViewUserAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Show all advice that has been given for a case
        """
        return get_case_advice(get_user_case_advice, request, self.case, "user")

    def post(self, request, **kwargs):
        return render_form_page(get_user_case_advice, request, self.case, self.form)


class GiveUserAdvice(TemplateView):
    """
    Select the type of advice
    """

    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form = give_advice_dispatch("user", request, **kwargs)
        return super(GiveUserAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice(get_user_case_advice, request, self.case, self.form, "user")


class GiveUserAdviceDetail(TemplateView):
    """
    Give details on the selection and send the data to the API
    """

    case = None
    form = "case/give-advice.html"

    def dispatch(self, request, *args, **kwargs):
        self.case = give_advice_detail_dispatch(request, **kwargs)
        return super(GiveUserAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice_details(post_user_case_advice, request, self.case, self.form, "user")


class CoalesceUserAdvice(TemplateView):
    """
    Group all of a user's team's user level advice in a team advie for the user's team
    """

    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        coalesce_user_advice(request, case_id)
        return redirect(reverse("cases:team_advice_view", kwargs={"pk": case_id}))


class ViewTeamAdvice(TemplateView):
    """
    View the user's team's team level advice or another team's, edit and clear the user's team's team level advice
    """

    case = None
    form = None
    team = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form, self.team = give_advice_dispatch("team", request, **kwargs)
        return super(ViewTeamAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Show all team advice given for a case
        """
        return get_case_advice(get_team_case_advice, request, self.case, "team", self.team)

    def post(self, request, **kwargs):
        if request.POST.get("action") == "delete":
            clear_team_advice(request, self.case.get("id"))

            return redirect(reverse("cases:team_advice_view", kwargs={"pk": self.case.get("id")}))

        elif request.POST.get("action") == "team":
            return get_case_advice(get_team_case_advice, request, self.case, "team", {"id": request.POST.get("team")})

        return render_form_page(get_team_case_advice, request, self.case, self.form, self.team)


class GiveTeamAdvice(TemplateView):
    """
    Select the type of advice
    """

    case = None
    form = None
    team = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form, self.team = give_advice_dispatch("team", request, **kwargs)
        return super(GiveTeamAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice(get_team_case_advice, request, self.case, self.form, "team", self.team)


class GiveTeamAdviceDetail(TemplateView):
    """
    Post the advice details to the API
    """

    case = None
    form = "case/give-advice.html"

    def dispatch(self, request, *args, **kwargs):
        self.case = give_advice_detail_dispatch(request, **kwargs)
        return super(GiveTeamAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice_details(post_team_case_advice, request, self.case, self.form, "team")


class CoalesceTeamAdvice(TemplateView):
    """
    Group all team's advice into final advice
    """

    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        coalesce_team_advice(request, case_id)
        return redirect(reverse("cases:final_advice_view", kwargs={"pk": case_id}))


class ViewFinalAdvice(TemplateView):
    """
    View, clear and edit final advice
    """

    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form = give_advice_dispatch("final", request, **kwargs)
        return super(ViewFinalAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Show all final advice given for a case
        """
        return get_case_advice(get_final_case_advice, request, self.case, "final")

    def post(self, request, **kwargs):
        if request.POST.get("action") == "delete":
            clear_final_advice(request, self.case.get("id"))

            return redirect(reverse("cases:final_advice_view", kwargs={"pk": self.case.get("id")}))

        return render_form_page(get_final_case_advice, request, self.case, self.form)


class GiveFinalAdvice(TemplateView):
    """
    Select advice type
    """

    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form = give_advice_dispatch("final", request, **kwargs)
        return super(GiveFinalAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice(get_final_case_advice, request, self.case, self.form, "final")


class GiveFinalAdviceDetail(TemplateView):
    """
    Post the advice details to the API
    """

    case = None
    form = "case/give-advice.html"

    def dispatch(self, request, *args, **kwargs):
        self.case = give_advice_detail_dispatch(request, **kwargs)
        return super(GiveFinalAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice_details(post_final_case_advice, request, self.case, self.form, "final")


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
        return render(request, "case/finalise-open-goods-countries.html", context)

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
            return render(request, "case/finalise-open-goods-countries.html", context)

        data, _ = post_good_countries_decisions(request, str(kwargs["pk"]), selection)

        if action == "save":
            context["good_countries"] = data["data"]
            return render(request, "case/finalise-open-goods-countries.html", context)
        elif "errors" in data:
            context["error"] = data.get("errors")
            return render(request, "case/finalise-open-goods-countries.html", context)

        return redirect(reverse_lazy("cases:finalise", kwargs={"pk": kwargs["pk"]}))


class Finalise(TemplateView):
    """
    Finalise a case and change the case status to finalised
    """

    def get(self, request, *args, **kwargs):
        case = get_case(request, str(kwargs["pk"]))
        case_type = case["application"]["case_type"]["sub_type"]

        if case_type == CaseType.STANDARD.value or case_type == CaseType.EXHIBITION.value:
            advice, _ = get_final_case_advice(request, str(kwargs["pk"]))
            data = advice["advice"]
            search_key = "type"
            is_open_licence = False
        else:
            data = get_good_countries_decisions(request, str(kwargs["pk"]))["data"]
            search_key = "decision"
            is_open_licence = True

        case_id = case["id"]
        duration = get_application_default_duration(request, str(kwargs["pk"]))

        for item in data:
            if item[search_key]["key"] == "approve" or item[search_key]["key"] == "proviso":
                today = date.today()

                form_data = {
                    "day": today.day,
                    "month": today.month,
                    "year": today.year,
                    "licence_duration": duration,
                }
                form = approve_licence_form(
                    case_id=case_id,
                    is_open_licence=is_open_licence,
                    duration=duration,
                    editable_duration=helpers.has_permission(request, Permission.MANAGE_LICENCE_DURATION),
                )
                return form_page(request, form, data=form_data)

        return form_page(request, deny_licence_form(case_id, is_open_licence))

    def post(self, request, *args, **kwargs):
        case = get_case(request, str(kwargs["pk"]))
        is_open_licence = case["application"]["casetype"]["sub_type"] == CaseType.OPEN.value
        application_id = case.get("application").get("id")
        data = request.POST.copy()

        has_permission = helpers.has_permission(request, Permission.MANAGE_LICENCE_DURATION)

        res = finalise_application(request, application_id, data)

        if res.status_code == 403:
            return error_page(request, "You do not have permission.")

        if res.status_code == 400:
            form = approve_licence_form(
                case_id=case["id"],
                is_open_licence=is_open_licence,
                duration=data.get("licence_duration") or get_application_default_duration(request, str(kwargs["pk"])),
                editable_duration=has_permission,
            )
            return form_page(request, form, data=data, errors=res.json()["errors"])

        return redirect(reverse_lazy("cases:case", kwargs={"pk": case["id"]}))
