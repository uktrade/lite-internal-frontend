from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from cases.services import get_good, get_good_activity, put_good_flags
from flags.services import get_flags_good_level_for_team


class Good(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        good_pk = str(kwargs['good_pk'])
        good, status_code = get_good(request, good_pk)
        activity, status_code = get_good_activity(request, good_pk)

        context = {
            'case_id': case_id,
            'good': good['good'],
            'activity': activity['activity']
        }

        return render(request, 'cases/case/good.html', context)


class AssignGoodsFlags(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        good_id = str(kwargs['good_pk'])
        good_data, status_code = get_good(request, good_id)
        good_level_team_flags_data, status_code = get_flags_good_level_for_team(request)
        good_flags = good_data.get('good').get('flags')
        good_level_team_flags = good_level_team_flags_data.get('flags')

        for flag in good_level_team_flags:
            for good_flag in good_flags:
                flag['selected'] = flag['id'] in good_flag
                if flag['selected']:
                    break

        context = {
            'case_id': case_id,
            'good_id': good_id,
            'good_level_team_flags': good_level_team_flags
        }
        return render(request, 'cases/case/good_flags.html', context)

    def post(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        good_id = str(kwargs['good_pk'])
        flags = request.POST.getlist('flags[]')

        response, status_code = put_good_flags(request, good_id, {'flags': flags, 'note': request.POST.get('note')})

        if status_code != 201:
            good_level_team_flags_data, status_code = get_flags_good_level_for_team(request)

            context = {
                'case_id': case_id,
                'good_id': good_id,
                'good_level_team_flags': good_level_team_flags_data.get('flags'),
                'errors': response
            }
            return render(request, 'cases/case/good_flags.html', context)

        return redirect(reverse('cases:good', kwargs={'pk': case_id, 'good_pk': good_id}))
