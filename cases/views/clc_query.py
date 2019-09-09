from django.shortcuts import render
from django.views.generic import TemplateView
from lite_forms.generators import form_page

from cases.forms.respond_to_clc_query import respond_to_clc_query_form
from cases.services import get_case


class Respond(TemplateView):

    case_id = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case = get_case(request, self.case_id)
        self.form = respond_to_clc_query_form(case)

        return super(Respond, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form)

    def post(self, request, **kwargs):
        return render(request, 'cases/case/clc_query_overview.html', {'title': 'Response Overview'})
