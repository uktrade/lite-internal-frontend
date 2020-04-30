from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from conf.constants import Permission, FlagLevels
from core.helpers import has_permission
from lite_forms.components import HiddenField
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form
from cases.forms.flags import flags_form
from cases.forms.respond_to_good_query import respond_to_clc_query_form, respond_to_grading_query_form

from cases.services import get_case, put_goods_query_clc, put_flag_assignments, put_goods_query_pv_grading
from core.services import get_user_permissions
from flags.services import get_goods_flags
from lite_forms.views import SingleFormView
from picklists.services import get_picklist_item


class RespondCLCQuery(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.context = {"case": case}
        self.form = respond_to_clc_query_form(request, kwargs["queue_pk"], case)
        self.action = put_goods_query_clc
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.success_message = "Reviewed successfully"

        if not has_permission(request, Permission.REVIEW_GOODS):
            return redirect(reverse_lazy("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk}))


class RespondPVGradingQuery(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.context = {"case": case}
        self.form = respond_to_grading_query_form(kwargs["queue_pk"], case)
        self.action = put_goods_query_pv_grading
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.success_message = "Reviewed successfully"

        if not has_permission(request, Permission.RESPOND_PV_GRADING):
            return redirect(reverse_lazy("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk}))


class RespondCLCFlags(TemplateView):
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case = get_case(request, str(kwargs["pk"]))
        self.form = flags_form(flags=get_goods_flags(request, True), level=FlagLevels.GOODS, origin="response", url="#")
        self.form.post_url = reverse_lazy("cases:respond_to_clc_query_flags", kwargs={"pk": self.case["id"]})

        return super(RespondCLCFlags, self).dispatch(request, *args, **kwargs)

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
            "data": request.POST,
            "case": get_case(request, str(kwargs["pk"])),  # Do another pull of case as case flags have changed
            "report_summary": get_picklist_item(request, request.POST["report_summary"]),
        }
        return render(request, "case/queries/clc-query-response-overview.html", context)


class RespondPVGradingFlags(TemplateView):
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case = get_case(request, str(kwargs["pk"]))
        self.form = flags_form(flags=get_goods_flags(request, True), level=FlagLevels.GOODS, origin="response", url="#")
        self.form.post_url = reverse_lazy("cases:respond_to_pv_grading_query_flags", kwargs={"pk": self.case["id"]})

        return super(RespondPVGradingFlags, self).dispatch(request, *args, **kwargs)

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
            "data": request.POST,
            "case": get_case(request, str(kwargs["pk"])),
        }
        return render(request, "case/queries/pv-grading-query-response-overview.html", context)
