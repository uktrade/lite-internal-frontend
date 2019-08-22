from django.contrib import messages
from django.http import Http404, HttpRequest
from django.middleware.csrf import rotate_token
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from cases.forms.advice import advice_recommendation_form
from cases.helpers import clean_advice
from cases.services import get_case, post_case_advice, get_case_advice
from core.services import get_denial_reasons
from libraries.forms.components import HiddenField
from libraries.forms.generators import form_page, error_page
from picklists.services import get_picklists


def add_hidden_advice_data(questions_list, data):
    questions_list.append(HiddenField('goods', data.getlist('goods')))
    questions_list.append(HiddenField('goods_types', data.getlist('goods_types')))
    questions_list.append(HiddenField('countries', data.getlist('countries')))
    questions_list.append(HiddenField('end_user', data.get('end_user', '')))
    questions_list.append(HiddenField('ultimate_end_users', data.getlist('ultimate_end_users')))
    return questions_list


def check_matching_advice(user_id, advice, goods_or_destinations):
    first_advice = None
    pre_data = None

    # Checks if the item of advice which is owned by the user is in the selected advice that they are trying to edit
    def is_in_goods_or_destinations(item, goods_or_destinations):
        goods_or_destinations = str(goods_or_destinations)
        if str(item.get('good')) in goods_or_destinations \
                or str(item.get('end_user')) in goods_or_destinations \
                or str(item.get('ultimate_end_user')) in goods_or_destinations \
                or str(item.get('goods_type')) in goods_or_destinations \
                or str(item.get('country')) in goods_or_destinations:
            return True
        return False

    # Pre-populate data only in the instance that all the data contained within all selected advice matches
    for item in [x for x in advice if x['user']['id'] == user_id and is_in_goods_or_destinations(x, goods_or_destinations)]:
        # Sets up the first piece of advice to compare against then skips to the next cycle of the loop
        if first_advice is None:
            first_advice = item
            pre_data = {
                'type': {
                    'key': first_advice['type']['key'],
                    'value': first_advice['type']['value']
                },
                'proviso': first_advice.get('proviso'),
                'denial_reasons': first_advice.get('denial_reasons'),
                'advice': first_advice.get('text'),
                'note': first_advice.get('note')
            }
            continue

        # End loop if any data does not match
        if not first_advice['type']['key'] == item['type']['key']:
            pre_data = None
            break
        else:
            if not first_advice.get('proviso') == item.get('proviso'):
                pre_data = None
                break
            if not first_advice.get('denial_reasons') == item.get('denial_reasons'):
                pre_data = None
                break
            if not first_advice.get('text') == item.get('text'):
                pre_data = None
                break
            if not first_advice.get('note') == item.get('note'):
                pre_data = None
                break

    return pre_data


class ViewAdvice(TemplateView):
    case_id = None
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case, _ = get_case(request, self.case_id)
        self.case = case['case']
        self.form = advice_recommendation_form(self.case_id)

        return super(ViewAdvice, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Show all advice given for a case
        """
        advice, status_code = get_case_advice(request, self.case_id)

        context = {
            'case': self.case,
            'title': self.case.get('application').get('name'),
            'all_advice': advice['advice'],
        }
        return render(request, 'cases/case/advice-view.html', context)

    def post(self, request, **kwargs):

        advice, status_code = get_case_advice(request, self.case_id)
        selected_advice_data = request.POST
        pre_data = check_matching_advice(request.user.lite_api_user_id, advice['advice'], selected_advice_data)

        # Validate at least one checkbox is checked
        if not len(selected_advice_data) > 1:
            return error_page(request, 'Select at least one good or destination to give advice on')

        # Add data to the form as hidden fields
        self.form.questions = add_hidden_advice_data(self.form.questions, selected_advice_data)

        return form_page(request, self.form, data=pre_data)


class GiveAdvice(TemplateView):
    case_id = None
    case = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        case, _ = get_case(request, self.case_id)
        self.case = case['case']
        self.form = advice_recommendation_form(self.case_id)

        return super(GiveAdvice, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        selected_advice_data = request.POST
        advice, status_code = get_case_advice(request, self.case_id)
        pre_data = check_matching_advice(request.user.lite_api_user_id, advice['advice'], selected_advice_data)

        if pre_data and not str(selected_advice_data['type']) in str(pre_data['type']):
            pre_data = None

        # Validate at least one radiobutton is selected
        if not selected_advice_data.get('type'):
            # Add data to the error form as hidden fields
            self.form.questions = add_hidden_advice_data(self.form.questions, selected_advice_data)

            return form_page(request, self.form, errors={'type': ['Select a decision']})

        # Render the advice detail page
        proviso_picklist_items, status_code = get_picklists(request, 'proviso')
        advice_picklist_items, status_code = get_picklists(request, 'standard_advice')
        static_denial_reasons, status_code = get_denial_reasons(request, False)

        self.form = 'cases/case/give-advice.html'

        context = {
            'case': self.case,
            'title': 'Give advice',
            'type': selected_advice_data.get('type'),
            'proviso_picklist': proviso_picklist_items['picklist_items'],
            'advice_picklist': advice_picklist_items['picklist_items'],
            'static_denial_reasons': static_denial_reasons,
            # Add previous data
            'goods': selected_advice_data.get('goods'),
            'goods_types': selected_advice_data.get('goods_types'),
            'countries': selected_advice_data.get('countries'),
            'end_user': selected_advice_data.get('end_user'),
            'ultimate_end_users': selected_advice_data.get('ultimate_end_users'),
            'data': pre_data,
        }
        return render(request, self.form, context)


class GiveAdviceDetail(TemplateView):
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

        return super(GiveAdviceDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        data = request.POST
        response, status_code = post_case_advice(request, self.case_id, data)

        if 'errors' in response:
            proviso_picklist_items, status_code = get_picklists(request, 'proviso')
            advice_picklist_items, status_code = get_picklists(request, 'standard_advice')
            static_denial_reasons, status_code = get_denial_reasons(request, False)

            data = clean_advice(data)

            context = {
                'case': self.case,
                'title': 'Error: Give advice',
                'type': data.get('type'),
                'proviso_picklist': proviso_picklist_items['picklist_items'],
                'advice_picklist': advice_picklist_items['picklist_items'],
                'static_denial_reasons': static_denial_reasons,
                # Add previous data
                'goods': data.get('goods'),
                'goods_types': data.get('goods_types'),
                'countries': data.get('countries'),
                'end_user': data.get('end_user'),
                'ultimate_end_users': data.get('ultimate_end_users'),
                'errors': response['errors'][0],
                'data': data,
            }
            return render(request, self.form, context)

        # Add success message
        messages.success(request, 'Your advice has been posted successfully')

        return redirect(reverse_lazy('cases:advice_view', kwargs={'pk': self.case_id}))
