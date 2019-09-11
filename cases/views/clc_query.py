from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form

from cases.forms.respond_to_clc_query import respond_to_clc_query_form
from cases.services import get_case, put_control_list_classification_query
from picklists.services import get_picklist_item


class Respond(TemplateView):
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case = get_case(request, str(kwargs['pk']))
        self.form = respond_to_clc_query_form(request, self.case)

        return super(Respond, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form)

    def post(self, request, **kwargs):
        print(request.POST)

        if request.POST.get('action') != 'change':
            response, data = submit_single_form(request,
                                                self.form,
                                                put_control_list_classification_query,
                                                pk=str(self.case['query']['id']))

            if response:
                return response

        # If validate only is removed (therefore the user is on the overview page
        # already) go back to the case and show a success message
        if not request.POST.get('validate_only'):
            if request.POST.get('action') == 'change':
                return form_page(request, self.form, data=request.POST)

            return redirect(reverse_lazy('cases:case', kwargs={'pk': self.case['id']}))

        # Remove validate only key and go to overview page
        data = request.POST.copy()
        del data['validate_only']

        context = {
            'title': 'Response Overview',
            'data': data,
            'case': self.case,
            'report_summary': get_picklist_item(request, data['report_summary'])
        }
        return render(request, 'cases/case/clc_query_overview.html', context)
