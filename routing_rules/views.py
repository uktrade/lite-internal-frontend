from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from lite_forms.components import FiltersBar, Option, Checkboxes
from lite_forms.views import MultiFormView
from routing_rules.forms import routing_rule_formgroup
from routing_rules.services import get_routing_rules, post_routing_rule
from users.services import get_gov_user


class RoutingRulesList(TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_routing_rules(request)
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
