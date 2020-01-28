from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.components import HiddenField
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form
from cases.forms.flags import flags_form
from cases.forms.respond_to_good_query import respond_to_clc_query_form, respond_to_grading_query_form

from cases.services import get_case, put_goods_query_clc, put_flag_assignments, put_goods_query_pv_grading
from core.services import get_user_permissions
from flags.services import get_goods_flags
from picklists.services import get_picklist_item


class RespondCLCQuery(TemplateView):
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        case_id = str(kwargs["pk"])
        self.case = get_case(request, case_id)
        self.form = respond_to_clc_query_form(request, self.case)

        permissions = get_user_permissions(request)
        if "REVIEW_GOODS" not in permissions:
            return redirect(reverse_lazy("cases:case", kwargs={"pk": case_id}))

        return super(RespondCLCQuery, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form)

    def post(self, request, **kwargs):
        # If 'set-flags' take them to the goods flags page
        if request.POST.get("action") == "set-flags":
            form = flags_form(flags=get_goods_flags(request, True), level="goods", origin="response", url="#")

            form.questions.append(HiddenField("is_good_controlled", request.POST["is_good_controlled"]))
            form.questions.append(HiddenField("control_code", request.POST.get("control_code")))
            form.questions.append(HiddenField("report_summary", request.POST["report_summary"]))
            form.questions.append(HiddenField("comment", request.POST["comment"]))

            form.post_url = reverse_lazy("cases:respond_to_clc_query_flags", kwargs={"pk": self.case["id"]})
            return form_page(request, form, data={"flags": self.case["query"]["good"]["flags"]})

        if request.POST.get("action") == "change":
            return form_page(request, self.form, data=request.POST)

        form_data = request.POST.copy()

        if request.POST.get("report_summary") == "None":
            del form_data["report_summary"]

        response, response_data = submit_single_form(
            request, self.form, put_goods_query_clc, object_pk=str(self.case["query"]["id"]), override_data=form_data,
        )

        if response:
            return response

        if not request.POST.get("validate_only"):
            return redirect(reverse_lazy("cases:case", kwargs={"pk": self.case["id"]}))

        response_data = response_data["control_list_classification_query"]
        # If validate only is removed (therefore the user is on the overview page
        # already) go back to the case and show a success message

        # Remove validate only key and go to overview page
        if response_data["is_good_controlled"] == "no":
            response_data.pop("control_code")

        context = {
            "title": "Response Overview",
            "data": response_data,
            "case": self.case,
        }

        if response_data.get("report_summary"):
            context["report_summary"] = get_picklist_item(request, response_data["report_summary"])

        return render(request, "case/queries/clc_query_response_overview.html", context)


class RespondPVGradingQuery(TemplateView):
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        case_id = str(kwargs["pk"])
        self.case = get_case(request, case_id)
        self.form = respond_to_grading_query_form(request, self.case)

        permissions = get_user_permissions(request)
        if "RESPOND_PV_GRADING" not in permissions:
            return redirect(reverse_lazy("cases:case", kwargs={"pk": case_id}))

        return super(RespondPVGradingQuery, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form)

    def post(self, request, **kwargs):
        # If 'set-flags' take them to the goods flags page
        if request.POST.get("action") == "set-flags":
            form = flags_form(flags=get_goods_flags(request, True), level="goods", origin="response", url="#")

            form.questions.append(HiddenField("is_good_controlled", request.POST["is_good_controlled"]))
            form.questions.append(HiddenField("control_code", request.POST.get("control_code")))
            form.questions.append(HiddenField("report_summary", request.POST["report_summary"]))
            form.questions.append(HiddenField("comment", request.POST["comment"]))

            form.post_url = reverse_lazy("cases:respond_to_clc_query_flags", kwargs={"pk": self.case["id"]})
            return form_page(request, form, data={"flags": self.case["query"]["good"]["flags"]})

        # original form posted
        if request.POST.get("action") == "change":
            return form_page(request, self.form, data=request.POST)

        form_data = request.POST.copy()

        response, response_data = submit_single_form(
            request,
            self.form,
            put_goods_query_pv_grading,
            object_pk=str(self.case["query"]["id"]),
            override_data=form_data,
        )

        if response:
            return response

        if not request.POST.get("validate_only"):
            return redirect(reverse_lazy("cases:case", kwargs={"pk": self.case["id"]}))

        response_data = response_data["pv_grading_query"]

        context = {
            "title": "Response Overview",
            "data": response_data,
            "case": self.case,
        }

        return render(request, "case/queries/pv_grading_query_response_overview.html", context)


class RespondFlags(TemplateView):
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case = get_case(request, str(kwargs["pk"]))
        self.form = flags_form(flags=get_goods_flags(request, True), level="goods", origin="response", url="#")
        self.form.post_url = reverse_lazy("cases:respond_to_clc_query_flags", kwargs={"pk": self.case["id"]})

        return super(RespondFlags, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        put_flag_assignments(
            request,
            {
                "level": "Goods",
                "objects": self.case["query"]["good"]["id"],
                "flags": request.POST.getlist("flags"),
                "note": request.POST.get("note"),
            },
        )

        context = {
            "title": "Response Overview",
            "data": request.POST,
            "case": get_case(request, str(kwargs["pk"])),  # Do another pull of case as case flags have changed
            "report_summary": get_picklist_item(request, request.POST["report_summary"]),
        }
        return render(request, "case/queries/clc_query_response_overview.html", context)
