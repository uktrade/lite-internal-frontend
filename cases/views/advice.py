from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from cases.forms.advice import advice_recommendation_form
from cases.services import get_case, post_user_case_advice, get_user_case_advice, get_team_case_advice, get_final_case_advice, coalesce_user_advice, coalesce_team_advice, clear_team_advice, clear_final_advice, post_team_case_advice, post_final_case_advice
from cases.views_helpers import get_case_advice, render_form_page, post_advice, post_advice_details
from users.services import get_gov_user


class ViewUserAdvice(TemplateView):
    case_id = None
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case, _ = get_case(request, self.case_id)
        self.case = case['case']
        self.form = advice_recommendation_form(reverse_lazy('cases:give_user_advice', kwargs={'pk': self.case_id}))

        return super(ViewUserAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Show all advice given for a case
        """
        return get_case_advice(get_user_case_advice, request, self.case, 'user')

    def post(self, request, **kwargs):
        return render_form_page(get_user_case_advice, request, self.case, self.form)


class CoalesceUserAdvice(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        coalesce_user_advice(request, case_id)
        return redirect(reverse('cases:team_advice_view', kwargs={'pk': case_id}))


class ViewTeamAdvice(TemplateView):
    case_id = None
    case = None
    form = None
    user = None
    team = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        self.user, _ = get_gov_user(request)
        self.team = self.user['user']['team']
        case, _ = get_case(request, self.case_id)
        self.case = case['case']
        self.form = advice_recommendation_form(self.case_id)

        return super(ViewTeamAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Show all advice given for a case
        """

        return get_case_advice(get_team_case_advice, request, self.case, 'team', self.team.get('id'))

    def post(self, request, **kwargs):

        if request.POST.get('action') == 'delete':
            clear_team_advice(request, self.case_id)

            return redirect(reverse('cases:team_advice_view', kwargs={'pk': self.case_id}))

        return render_form_page(get_team_case_advice, request, self.case, self.form, self.team.get('id'))


class CoalesceTeamAdvice(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        coalesce_team_advice(request, case_id)
        return redirect(reverse('cases:final_advice_view', kwargs={'pk': case_id}))


class ViewFinalAdvice(TemplateView):
    case_id = None
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case, _ = get_case(request, self.case_id)
        self.case = case['case']
        self.form = advice_recommendation_form(self.case_id)

        return super(ViewFinalAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Show all advice given for a case
        """
        return get_case_advice(get_final_case_advice, request, self.case, 'final')

    def post(self, request, **kwargs):

        if request.POST.get('action') == 'delete':
            clear_final_advice(request, self.case_id)

            return redirect(reverse('cases:final_advice_view', kwargs={'pk': self.case_id}))

        return render_form_page(get_final_case_advice, request, self.case, self.form)


class GiveUserAdvice(TemplateView):
    case_id = None
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case, _ = get_case(request, self.case_id)
        self.case = case['case']
        self.form = advice_recommendation_form(reverse_lazy('cases:give_user_advice', kwargs={'pk': self.case_id}))

        return super(GiveUserAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice(get_user_case_advice, request, self.case, self.form, 'user')


class GiveUserAdviceDetail(TemplateView):
    case_id = None
    case = None
    form = 'cases/case/give-advice.html'

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case, _ = get_case(request, self.case_id)
        self.case = case['case']

        # If the advice type is not valid, raise a 404
        advice_type = kwargs['type']
        if advice_type not in ['approve', 'proviso', 'refuse', 'no_licence_required', 'not_applicable']:
            raise Http404

        return super(GiveUserAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice_details(post_user_case_advice, request, self.case, self.form, 'user')


class GiveTeamAdvice(TemplateView):
    case_id = None
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case, _ = get_case(request, self.case_id)
        self.case = case['case']
        self.form = advice_recommendation_form(reverse_lazy('cases:give_team_advice', kwargs={'pk': self.case_id}))

        return super(GiveTeamAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice(get_team_case_advice, request, self.case, self.form, 'team')


class GiveTeamAdviceDetail(TemplateView):
    case_id = None
    case = None
    form = 'cases/case/give-advice.html'

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case, _ = get_case(request, self.case_id)
        self.case = case['case']

        # If the advice type is not valid, raise a 404
        advice_type = kwargs['type']
        if advice_type not in ['approve', 'proviso', 'refuse', 'no_licence_required', 'not_applicable']:
            raise Http404

        return super(GiveTeamAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice_details(post_team_case_advice, request, self.case, self.form, 'team')


class GiveFinalAdvice(TemplateView):
    case_id = None
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case, _ = get_case(request, self.case_id)
        self.case = case['case']
        self.form = advice_recommendation_form(reverse_lazy('cases:give_final_advice', kwargs={'pk': self.case_id}))

        return super(GiveFinalAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice(get_final_case_advice, request, self.case, self.form, 'final')


class GiveFinalAdviceDetail(TemplateView):
    case_id = None
    case = None
    form = 'cases/case/give-advice.html'

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case, _ = get_case(request, self.case_id)
        self.case = case['case']

        # If the advice type is not valid, raise a 404
        advice_type = kwargs['type']
        if advice_type not in ['approve', 'proviso', 'refuse', 'no_licence_required', 'not_applicable']:
            raise Http404

        return super(GiveFinalAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice_details(post_final_case_advice, request, self.case, self.form, 'final')
