from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from core.helpers import get_params_if_exist, convert_dict_to_query_params
from lite_forms.components import FiltersBar, Option, Checkboxes
from lite_forms.views import MultiFormView
from routing_rules.forms import routing_rule_formgroup
from routing_rules.services import get_routing_rules, post_routing_rule, put_routing_rule_status
from users.services import get_gov_user


class RoutingRulesList(TemplateView):
    def get(self, request, **kwargs):
        params = {"page": int(request.GET.get("page", 1))}

        data, _ = get_routing_rules(request, convert_dict_to_query_params(params))

        user_data, _ = get_gov_user(request, str(request.user.lite_api_user_id))

        status = request.GET.get("status", "active")

        filters = FiltersBar(
            [
                Checkboxes(
                    name="active", options=[Option("deactivated", "Deactivated")], classes=["govuk-checkboxes--small"],
                ),
            ]
        )

        context = {
            "data": data,
            "status": status,
            "user_data": user_data,
            "filters": filters,
        }
        return render(request, "routing_rules/index.html", context)


class CreateRoutingRule(MultiFormView):
    def init(self, request, **kwargs):
        if request.method == "POST":
            self.forms = routing_rule_formgroup(request, request.POST.getlist("additional_rules[]"))
        else:
            self.forms = routing_rule_formgroup(request)
        self.success_url = reverse("routing_rules:list")
        self.action = post_routing_rule


class ChangeRoutingRuleActiveStatus(TemplateView):
    def get(self, request, **kwargs):
        status = kwargs["status"]
        description = ""

        if status != "deactivate" and status != "reactivate":
            raise Http404

        if status == "deactivate":
            description = "you are deactivating the flag"

        if status == "reactivate":
            description = "you are reactivating the flag"

        context = {
            "title": "Are you sure you want to {} this routing rule?".format(status),
            "description": description,
            "user_id": str(kwargs["pk"]),
            "status": status,
        }
        return render(request, "routing_rules/change-status.html", context)

    def post(self, request, **kwargs):
        status = kwargs["status"]

        if status != "deactivate" and status != "reactivate":
            raise Http404

        put_routing_rule_status(request, str(kwargs["pk"]), status)

        return redirect(reverse_lazy("routing_rules:list"))
