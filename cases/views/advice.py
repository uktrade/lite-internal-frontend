from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from cases.services import post_user_case_advice, get_user_case_advice, get_team_case_advice, \
    get_final_case_advice, coalesce_user_advice, coalesce_team_advice, post_team_case_advice, post_final_case_advice, clear_team_advice, clear_final_advice
from cases.views_helpers import get_case_advice, render_form_page, post_advice, post_advice_details, give_advice_detail_dispatch, give_advice_dispatch, view_advice_dispatch


class ViewUserAdvice(TemplateView):
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form = view_advice_dispatch('user', request, **kwargs)
        return super(ViewUserAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Show all advice given for a case
        """
        return get_case_advice(get_user_case_advice, request, self.case, 'user')

    def post(self, request, **kwargs):
        return render_form_page(get_user_case_advice, request, self.case, self.form)


class GiveUserAdvice(TemplateView):
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form = give_advice_dispatch('user', request, **kwargs)
        return super(GiveUserAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice(get_user_case_advice, request, self.case, self.form, 'user')


class GiveUserAdviceDetail(TemplateView):
    case = None
    form = 'cases/case/give-advice.html'

    def dispatch(self, request, *args, **kwargs):
        self.case = give_advice_detail_dispatch(request, **kwargs)
        return super(GiveUserAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice_details(post_user_case_advice, request, self.case, self.form, 'user')


class CoalesceUserAdvice(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        coalesce_user_advice(request, case_id)
        return redirect(reverse('cases:team_advice_view', kwargs={'pk': case_id}))


class ViewTeamAdvice(TemplateView):
    case = None
    form = None
    team = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form, self.team = view_advice_dispatch('team', request, **kwargs)
        return super(ViewTeamAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Show all team advice given for a case
        """
        return get_case_advice(get_team_case_advice, request, self.case, 'team', self.team)

    def post(self, request, **kwargs):
        if request.POST.get('action') == 'delete':
            clear_team_advice(request, self.case.get('id'))

            return redirect(reverse('cases:team_advice_view', kwargs={'pk': self.case.get('id')}))

        return render_form_page(get_team_case_advice, request, self.case, self.form, self.team)


class GiveTeamAdvice(TemplateView):
    case = None
    form = None
    team = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form, self.team = give_advice_dispatch('team', request, **kwargs)
        return super(GiveTeamAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice(get_team_case_advice, request, self.case, self.form, 'team', self.team)


class GiveTeamAdviceDetail(TemplateView):
    case = None
    form = 'cases/case/give-advice.html'

    def dispatch(self, request, *args, **kwargs):
        self.case = give_advice_detail_dispatch(request, **kwargs)
        return super(GiveTeamAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice_details(post_team_case_advice, request, self.case, self.form, 'team')


class CoalesceTeamAdvice(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        coalesce_team_advice(request, case_id)
        return redirect(reverse('cases:final_advice_view', kwargs={'pk': case_id}))


class ViewFinalAdvice(TemplateView):
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form = view_advice_dispatch('final', request, **kwargs)
        return super(ViewFinalAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Show all final advice given for a case
        """
        return get_case_advice(get_final_case_advice, request, self.case, 'final')

    def post(self, request, **kwargs):
        if request.POST.get('action') == 'delete':
            clear_final_advice(request, self.case.get('id'))

            return redirect(reverse('cases:final_advice_view', kwargs={'pk': self.case.get('id')}))

        return render_form_page(get_final_case_advice, request, self.case, self.form)


class GiveFinalAdvice(TemplateView):
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form = give_advice_dispatch('final', request, **kwargs)
        return super(GiveFinalAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice(get_final_case_advice, request, self.case, self.form, 'final')


class GiveFinalAdviceDetail(TemplateView):
    case = None
    form = 'cases/case/give-advice.html'

    def dispatch(self, request, *args, **kwargs):
        self.case = give_advice_detail_dispatch(request, **kwargs)
        return super(GiveFinalAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice_details(post_final_case_advice, request, self.case, self.form, 'final')
