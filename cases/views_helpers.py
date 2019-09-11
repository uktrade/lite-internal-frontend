from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from lite_forms.generators import error_page, form_page

from cases.helpers import check_matching_advice, add_hidden_advice_data, clean_advice
from core.services import get_denial_reasons
from picklists.services import get_picklists


def get_case_advice(get_advice, request, case, user_team_final, team=None):
    if team:
        advice, status_code = get_advice(request, case.get('id'), team)
    else:
        advice, status_code = get_advice(request, case.get('id'))

    context = {
        'case': case,
        'title': case.get('application').get('name'),
        'all_advice': advice['advice'],
    }
    return render(request, 'cases/case/' + user_team_final + '-advice-view.html', context)


def render_form_page(get_advice, request, case, form, team=None):
    if team:
        advice, status_code = get_advice(request, case.get('id'), team)
    else:
        advice, status_code = get_advice(request, case.get('id'))

    selected_advice_data = request.POST
    pre_data = check_matching_advice(request.user.lite_api_user_id, advice['advice'], selected_advice_data)

    # Validate at least one checkbox is checked
    if not len(selected_advice_data) > 0:
        return error_page(request, 'Select at least one good or destination to give advice on')

    # Add data to the form as hidden fields
    form.questions = add_hidden_advice_data(form.questions, selected_advice_data)

    return form_page(request, form, data=pre_data)


def post_advice(get_advice, request, case, form, user_team_final, team=None):
    selected_advice_data = request.POST
    if team:
        advice, status_code = get_advice(request, case.get('id'), team)
    else:
        advice, status_code = get_advice(request, case.get('id'))
    pre_data = check_matching_advice(request.user.lite_api_user_id, advice['advice'], selected_advice_data)

    if pre_data and not str(selected_advice_data['type']) in str(pre_data['type']):
        pre_data = None

    # Validate at least one radiobutton is selected
    if not selected_advice_data.get('type'):
        # Add data to the error form as hidden fields
        form.questions = add_hidden_advice_data(form.questions, selected_advice_data)

        return form_page(request, form, errors={'type': ['Select a decision']})

    # Render the advice detail page
    proviso_picklist_items, status_code = get_picklists(request, 'proviso')
    advice_picklist_items, status_code = get_picklists(request, 'standard_advice')
    static_denial_reasons, status_code = get_denial_reasons(request, False)

    form = 'cases/case/give-advice.html'

    context = {
        'case': case,
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
        'level': user_team_final
    }
    return render(request, form, context)


def post_advice_details(post_case_advice, request, case, form, user_team_final):
    data = request.POST
    response, status_code = post_case_advice(request, case.get('id'), data)

    if 'errors' in response:
        proviso_picklist_items, status_code = get_picklists(request, 'proviso')
        advice_picklist_items, status_code = get_picklists(request, 'standard_advice')
        static_denial_reasons, status_code = get_denial_reasons(request, False)

        data = clean_advice(data)

        context = {
            'case': case,
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
        return render(request, form, context)

    # Add success message
    messages.success(request, 'Your advice has been posted successfully')

    return redirect(reverse_lazy('cases:' + user_team_final + '_advice_view', kwargs={'pk': case.get('id')}))