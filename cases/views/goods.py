from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from cases.forms.goods_flags import goods_flags_form
from cases.services import get_good, get_good_activity, put_good_flags
from flags.services import get_flags_good_level_for_team
from libraries.forms.components import Option
from libraries.forms.generators import form_page


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

    goods = None
    form = None
    selected_flags = None
    url = None

    def dispatch(self, request, *args, **kwargs):
        case_id = str(kwargs['pk'])
        kwargs = {'pk': case_id}
        self.goods = request.GET.getlist('goods')
        good_or_case = request.GET.get('good_or_case') if request.GET.get('good_or_case') else 'case'

        if not self.goods:
            raise Http404

        good_level_team_flags_data, status_code = get_flags_good_level_for_team(request)

        good_level_team_flags = [x for x in good_level_team_flags_data.get('flags') if x['status'] == 'Active']

        if len(self.goods) == 1:
            good, status_code = get_good(request, pk=self.goods[0])
            good_flags = good.get('good').get('flags')
            self.selected_flags = {'flags': []}
            for flag in good_level_team_flags:
                for good_flag in good_flags:
                    if flag['id'] in good_flag['id']:
                        self.selected_flags['flags'].append(flag['id'])
                        break
            if good_or_case == 'good':
                kwargs = {'pk': case_id, 'good_pk': self.goods[0]}

        flags = [Option(x['id'], x['name']) for x in good_level_team_flags]
        self.url = reverse('cases:' + good_or_case, kwargs=kwargs)

        self.form = goods_flags_form(
            flags=flags,
            good_or_case=good_or_case,
            url=self.url
        )

        return super(AssignGoodsFlags, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form, data=self.selected_flags)

    def post(self, request, **kwargs):
        response, status_code = put_good_flags(request, {'goods': self.goods, 'flags': request.POST.getlist('flags'), 'note': request.POST.get('note')})

        if 'errors' in response:
            return form_page(request, self.form, data=request.POST, errors=response['errors'])

        return redirect(self.url)
