from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from cases.forms.advice import advice_recommendation_form
from cases.services import get_case
from libraries.forms.generators import form_page
from picklists.services import get_picklists


class ViewAdvice(TemplateView):
    case_id = None
    case = None
    form = advice_recommendation_form()

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case, _ = get_case(request, self.case_id)
        self.case = case['case']
        # permissions = get_user_permissions(request)

        return super(ViewAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        context = {
            'case': self.case,
            'title': self.case.get('application').get('name'),
        }
        return render(request, 'cases/case/advice-view.html', context)


class GiveAdvice(TemplateView):
    case = None
    form = advice_recommendation_form()

    def dispatch(self, request, *args, **kwargs):
        case_id = str(kwargs['pk'])
        case, _ = get_case(request, case_id)
        self.case = case['case']

        return super(GiveAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form)

    def post(self, request, **kwargs):
        data = request.POST

        if not data.get('type'):
            return form_page(request, self.form, errors={'type': ['Select a decision']})

        return redirect(reverse_lazy('cases:give_advice_detail', kwargs={'pk': self.case['id'], 'type': data['type']}))


class GiveAdviceDetail(TemplateView):
    case = None
    form = 'cases/case/give-advice.html'
    type = ''

    def dispatch(self, request, *args, **kwargs):
        case_id = str(kwargs['pk'])
        case, _ = get_case(request, case_id)
        self.case = case['case']
        self.type = kwargs['type']

        # If the type is not valid, raise a 404
        if self.type not in ['approve', 'proviso', 'refuse', 'nlr', 'revoke', 'suspend', 'na']:
            raise Http404

        return super(GiveAdviceDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        case, _ = get_case(request, case_id)

        proviso_picklist_items, status_code = get_picklists(request, 'proviso')
        advice_picklist_items, status_code = get_picklists(request, 'standard_advice')

        context = {
            'case': case['case'],
            'title': 'Give advice',
            'type': self.type,
            'proviso_picklist': proviso_picklist_items['picklist_items'],
            'advice_picklist': advice_picklist_items['picklist_items'],
        }
        return render(request, self.form, context)
