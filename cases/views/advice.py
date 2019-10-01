from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page, error_page

from cases.forms.finalise_case import approve_licence_form, refuse_licence_form
from cases.services import post_user_case_advice, get_user_case_advice, get_team_case_advice, \
    get_final_case_advice, coalesce_user_advice, coalesce_team_advice, post_team_case_advice, \
    post_final_case_advice, clear_team_advice, clear_final_advice, get_case, put_applications, post_good_countries_decisions, get_good_countries_decisions
from cases.views_helpers import get_case_advice, render_form_page, post_advice, post_advice_details, \
    give_advice_detail_dispatch, give_advice_dispatch


class ViewUserAdvice(TemplateView):
    """
    view advice at a user level and select advice to edit
    """
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form = give_advice_dispatch('user', request, **kwargs)
        return super(ViewUserAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Show all advice given for a case
        """
        return get_case_advice(get_user_case_advice, request, self.case, 'user')

    def post(self, request, **kwargs):
        return render_form_page(get_user_case_advice, request, self.case, self.form)


class GiveUserAdvice(TemplateView):
    """
    Select the type of advice
    """
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form = give_advice_dispatch('user', request, **kwargs)
        return super(GiveUserAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice(get_user_case_advice, request, self.case, self.form, 'user')


class GiveUserAdviceDetail(TemplateView):
    """
    Give details on the selection and send the data to the API
    """
    case = None
    form = 'cases/case/give-advice.html'

    def dispatch(self, request, *args, **kwargs):
        self.case = give_advice_detail_dispatch(request, **kwargs)
        return super(GiveUserAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice_details(post_user_case_advice, request, self.case, self.form, 'user')


class CoalesceUserAdvice(TemplateView):
    """
    Group all of a user's team's user level advice in a team advie for the user's team
    """

    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        coalesce_user_advice(request, case_id)
        return redirect(reverse('cases:team_advice_view', kwargs={'pk': case_id}))


class ViewTeamAdvice(TemplateView):
    """
    View the user's team's team level advice or another team's, edit and clear the user's team's team level advice
    """
    case = None
    form = None
    team = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form, self.team = give_advice_dispatch('team', request, **kwargs)
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

        elif request.POST.get('action') == 'team':
            return get_case_advice(get_team_case_advice, request, self.case, 'team', {'id': request.POST.get('team')})

        return render_form_page(get_team_case_advice, request, self.case, self.form, self.team)


class GiveTeamAdvice(TemplateView):
    """
    Select the type of advice
    """
    case = None
    form = None
    team = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form, self.team = give_advice_dispatch('team', request, **kwargs)
        return super(GiveTeamAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice(get_team_case_advice, request, self.case, self.form, 'team', self.team)


class GiveTeamAdviceDetail(TemplateView):
    """
    Post the advice details to the API
    """
    case = None
    form = 'cases/case/give-advice.html'

    def dispatch(self, request, *args, **kwargs):
        self.case = give_advice_detail_dispatch(request, **kwargs)
        return super(GiveTeamAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice_details(post_team_case_advice, request, self.case, self.form, 'team')


class CoalesceTeamAdvice(TemplateView):
    """
    Group all team's advice into final advice
    """

    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        coalesce_team_advice(request, case_id)
        return redirect(reverse('cases:final_advice_view', kwargs={'pk': case_id}))


class ViewFinalAdvice(TemplateView):
    """
    View, clear and edit final advice
    """
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form = give_advice_dispatch('final', request, **kwargs)
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
    """
    Select advice type
    """
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case, self.form = give_advice_dispatch('final', request, **kwargs)
        return super(GiveFinalAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice(get_final_case_advice, request, self.case, self.form, 'final')


class GiveFinalAdviceDetail(TemplateView):
    """
    Post the advice details to the API
    """
    case = None
    form = 'cases/case/give-advice.html'

    def dispatch(self, request, *args, **kwargs):
        self.case = give_advice_detail_dispatch(request, **kwargs)
        return super(GiveFinalAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        return post_advice_details(post_final_case_advice, request, self.case, self.form, 'final')


class FinaliseGoodsCountries(TemplateView):
    @staticmethod
    def _generate_data(request, pk):
        case = get_case(request, pk)
        _advice, _ = get_final_case_advice(request, pk)

        # The keys are each relevant good-country pairing in the format good_id.country_id
        keys = []
        # Builds form page data structure
        # For each good in the case
        for good in case['application']['goods_types']:
            # Match the goods with the goods in advice for that case
            # and attach the advice value to the good
            for advice in _advice['advice']:
                if advice['goods_type'] == good['id']:
                    good['advice'] = advice['type']
            # If the good has countries attached to it as destinations
            # We do the same with the countries and their advice
            if good['countries']:
                for country in good['countries']:
                    keys.append(str(good['id']) + '.' + country['id'])
                    for advice in _advice['advice']:
                        if advice['country'] == country['id']:
                            country['advice'] = advice['type']
            # If the good has no countries:
            else:
                good['countries'] = []
                # We attach all countries from the case
                # And then attach the advice as before
                for country in case['application']['destinations']['data']:
                    good['countries'].append(country)
                    keys.append(str(good['id']) + '.' + country['id'])
                    for advice in _advice['advice']:
                        if advice['country'] == country['id']:
                            country['advice'] = advice['type']
        data = get_good_countries_decisions(request, pk)
        print('data1', data)
        if 'detail' in data:
            return error_page(request, 'You do not have permission.')

        return case, data, keys

    @staticmethod
    def _generate_errors(keys, request_data, action):
        post_data = []
        errors = {}
        for key in keys:
            good_pk = key.split('.')[0]
            country_pk = key.split('.')[1]
            if key not in request_data and not action == 'save':
                if good_pk in errors:
                    errors[good_pk].append(country_pk)
                else:
                    errors[good_pk] = [country_pk]
            else:
                post_data.append({'good': good_pk,
                                  'country': country_pk,
                                  'decision': request_data.get(key)})
        return post_data, errors

    def get(self, request, *args, **kwargs):
        case, data, _ = self._generate_data(request, str(kwargs['pk']))
        context = {
            'case': case,
            'good_countries': data['data'],
            'decisions': ['approve', 'refuse', 'no_licence_required'],
        }
        return render(request, 'cases/case/finalise-open-goods-countries.html', context)

    def post(self, request, *args, **kwargs):
        case, data, keys = self._generate_data(request, str(kwargs['pk']))

        request_data = request.POST.copy()
        request_data.pop('csrfmiddlewaretoken')
        selection = {}
        action = request_data.pop('action')[0]

        selection['good_countries'] = []
        for key, value in request_data.items():
            selection['good_countries'].append(
                {
                    'case': str(kwargs['pk']),
                    'good': key.split('.')[0],
                    'country': key.split('.')[1],
                    'decision': value}
            )

        context = {
            'case': case,
            'decisions': ['approve', 'refuse', 'no_licence_required'],
            'good_countries': data['data'],
            'errors': {}
        }

        post_data, errors = self._generate_errors(keys, request_data, action)

        # If errors, return page
        if errors:
            context['errors'] = errors
            context['good_countries'] = post_data
            return render(request, 'cases/case/finalise-open-goods-countries.html', context)

        data, _ = post_good_countries_decisions(request, str(kwargs['pk']), selection)

        if action == 'save':
            print(action)
            return render(request, 'cases/case/finalise-open-goods-countries.html', context)
        elif 'errors' in data:
            context['error'] = data.get('errors')
            return render(request, 'cases/case/finalise-open-goods-countries.html', context)

        return redirect(reverse_lazy('cases:finalise', kwargs={'pk': kwargs['pk']}))


class Finalise(TemplateView):
    """
    Finalise a case and change the case status to finalised
    """

    def get(self, request, *args, **kwargs):
        case = get_case(request, str(kwargs['pk']))
        standard = case['application']['licence_type']['key'] == 'standard_licence'
        if standard:
            advice, _ = get_final_case_advice(request, str(kwargs['pk']))
            data = advice['advice']
            search_key = 'type'
        else:
            data = get_good_countries_decisions(request, str(kwargs['pk']))['data']
            search_key = 'decision'

        case_id = case['id']

        for item in data:
            if item[search_key]['key'] == 'approve' or item[search_key]['key'] == 'proviso':
                return form_page(request, approve_licence_form(case_id, standard))

        return form_page(request, refuse_licence_form(case_id, standard))

    def post(self, request, *args, **kwargs):
        case = get_case(request, str(kwargs['pk']))
        application_id = case.get('application').get('id')
        data = request.POST.copy()
        data['status'] = 'finalised'
        put_applications(request, application_id, data)

        return redirect(reverse_lazy('cases:case', kwargs={'pk': case['id']}))
