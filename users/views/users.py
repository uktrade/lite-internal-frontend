from core.helpers import convert_dict_to_query_params
from lite_content.lite_internal_frontend import strings
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from conf.constants import SUPER_USER_ROLE_ID
from lite_forms.components import FiltersBar, Select, Option
from lite_forms.generators import form_page
from users.forms.users import add_user_form, edit_user_form
from users.services import (
    get_gov_users,
    post_gov_users,
    put_gov_user,
    get_gov_user,
    is_super_user,
)


class UsersList(TemplateView):
    def get(self, request, **kwargs):
        status = request.GET.get("status", "active")
        params = {"page": int(request.GET.get("page", 1)), "status": status}

        data, _ = get_gov_users(request, params)

        user, _ = get_gov_user(request, str(request.user.lite_api_user_id))
        super_user = is_super_user(user)

        statuses = [Option(option["key"], option["value"])for option in data["results"]["filters"]["status"]]
        filters = FiltersBar([Select(name="status", title="status", options=statuses)])

        context = {
            "data": data,
            "title": "Users",
            "super_user": super_user,
            "status": status,
            "page": params.pop("page"),
            "params_str": convert_dict_to_query_params(params),
            "filters": filters
        }

        return render(request, "users/index.html", context)


class AddUser(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, add_user_form(request))

    def post(self, request, **kwargs):
        response, status_code = post_gov_users(request, request.POST)

        if status_code != 201:
            return form_page(request, add_user_form(request), data=request.POST, errors=response.get("errors"))

        return redirect(reverse_lazy("users:users"))


class ViewUser(TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_gov_user(request, str(kwargs["pk"]))
        request_user, _ = get_gov_user(request, str(request.user.lite_api_user_id))
        super_user = is_super_user(request_user)
        can_deactivate = not is_super_user(data)

        context = {
            "data": data,
            "super_user": super_user,
            "super_user_role_id": SUPER_USER_ROLE_ID,
            "can_deactivate": can_deactivate,
        }
        return render(request, "users/profile.html", context)


class ViewProfile(TemplateView):
    def get(self, request, **kwargs):
        user = request.user
        return redirect(reverse_lazy("users:user", kwargs={"pk": user.id}))


class EditUser(TemplateView):
    def get(self, request, **kwargs):
        user, _ = get_gov_user(request, str(kwargs["pk"]))
        can_edit_role = user["user"]["id"] != request.user.lite_api_user_id
        return form_page(request, edit_user_form(request, str(kwargs["pk"]), can_edit_role), data=user["user"])

    def post(self, request, **kwargs):
        response, status_code = put_gov_user(request, str(kwargs["pk"]), request.POST)
        user, _ = get_gov_user(request, str(kwargs["pk"]))
        can_edit_role = user["user"]["id"] != request.user.lite_api_user_id

        if status_code != 200:
            return form_page(
                request,
                edit_user_form(request, str(kwargs["pk"]), can_edit_role),
                data=request.POST,
                errors=response.get("errors"),
            )

        return redirect(reverse_lazy("users:users"))


class ChangeUserStatus(TemplateView):
    def get(self, request, **kwargs):
        status = kwargs["status"]
        description = ""

        if status != "deactivate" and status != "reactivate":
            raise Http404

        if status == "deactivate":
            description = strings.UpdateUser.Status.DEACTIVATE_WARNING

        if status == "reactivate":
            description = strings.UpdateUser.Status.REACTIVATE_WARNING

        context = {
            "title": "Are you sure you want to {} this flag?".format(status),
            "description": description,
            "user_id": str(kwargs["pk"]),
            "status": status,
        }
        return render(request, "users/change_status.html", context)

    def post(self, request, **kwargs):
        status = kwargs["status"]

        if status != "deactivate" and status != "reactivate":
            raise Http404

        put_gov_user(request, str(kwargs["pk"]), json={"status": request.POST["status"]})

        return redirect("/users/")
