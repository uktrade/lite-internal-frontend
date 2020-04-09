from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from conf.constants import Permission
from core.helpers import convert_dict_to_query_params, has_permission, get_params_if_exist
from core.services import get_statuses
from lite_forms.components import FiltersBar, Option, Checkboxes, Select, AutocompleteInput, TextInput
from lite_forms.generators import form_page
from lite_forms.helpers import conditional
from lite_forms.views import MultiFormView, SingleFormView
from queues.services import get_queues
from routing_rules.forms import routing_rule_form_group, deactivate_or_activate_routing_rule_form
from routing_rules.services import (
    get_routing_rules,
    post_routing_rule,
    put_routing_rule_active_status,
    get_routing_rule,
    put_routing_rule,
    validate_put_routing_rule,
)
from teams.services import get_teams, get_users_team_queues
from users.services import get_gov_user


class RoutingRulesList(TemplateView):
    def get(self, request, **kwargs):
        params = {"page": int(request.GET.get("page", 1))}
        params = get_params_if_exist(request, ["case_status", "team", "queue", "tier", "only_active"], params)

        data, _ = get_routing_rules(request, convert_dict_to_query_params(params))

        user_data, _ = get_gov_user(request, str(request.user.lite_api_user_id))

        status = request.GET.get("status", "active")

        filters = FiltersBar(
            [
                Select(title="Case Status", name="case_status", options=get_statuses(request, True),),
                *conditional(
                    has_permission(request, Permission.MANAGE_ALL_ROUTING_RULES),
                    [
                        Select(title="Team", name="team", options=get_teams(request, True)),
                        AutocompleteInput(
                            title="Queue", name="queue", options=get_queues(request, convert_to_options=True),
                        ),
                    ],
                    [
                        AutocompleteInput(
                            title="Queue",
                            name="queue",
                            options=get_users_team_queues(request, request.user.lite_api_user_id, True),
                        ),
                    ],
                ),
                TextInput(title="Enter a tier number", name="tier"),
                Checkboxes(
                    name="only_active", options=[Option(True, "Only show active")], classes=["govuk-checkboxes--small"],
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
            self.forms = routing_rule_form_group(request, request.POST.getlist("additional_rules[]"))
        else:
            self.forms = routing_rule_form_group(request, list())
        self.success_url = reverse("routing_rules:list")
        self.action = post_routing_rule


class ChangeRoutingRuleActiveStatus(SingleFormView):
    success_url = reverse_lazy("routing_rules:list")

    def init(self, request, **kwargs):
        status = kwargs["status"]
        self.object_pk = kwargs["pk"]

        if status != "deactivate" and status != "reactivate":
            raise Http404

        if status == "deactivate":
            title = "Are you sure you want to deactivate this routing rule?"
            description = "you are deactivating the routing rule"
            confirm = "deactivate this routing rule"
        else:
            title = "Are you sure you want to activate this routing rule?"
            description = "you are deactivating the routing rule"
            confirm = "activate this routing rule"

        self.form = deactivate_or_activate_routing_rule_form(
            title=title, description=description, confirm_text=confirm, status=status
        )
        self.action = put_routing_rule_active_status

    def post(self, request, **kwargs):
        self.init(request, **kwargs)
        if not request.POST.get("confirm"):
            return form_page(
                request,
                self.get_form(),
                data=self.get_data(),
                errors={"confirm": ["Select to confirm or not"]},
                extra_data=self.context,
            )
        elif request.POST.get("confirm") == "no":
            return redirect(self.success_url)

        return super(ChangeRoutingRuleActiveStatus, self).post(request, **kwargs)


class EditRoutingRules(MultiFormView):
    def init(self, request, **kwargs):
        if request.method == "POST":
            additional_rules = request.POST.getlist("additional_rules[]", [])
            self.forms = routing_rule_form_group(request, additional_rules, is_editing=True)

            # we only want to update the data during the last form post
            if (len(self.get_forms().forms) - 1) == int(request.POST.get("form_pk", 0)):
                self.action = put_routing_rule
            else:
                self.action = validate_put_routing_rule

        else:
            self.forms = routing_rule_form_group(request, list(), is_editing=True)
            self.action = put_routing_rule

        self.object_pk = kwargs["pk"]
        self.data = get_routing_rule(request, self.object_pk)[0]
        self.success_url = reverse_lazy("routing_rules:list")
