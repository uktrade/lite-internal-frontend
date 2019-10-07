from django.shortcuts import render
from django.views.generic import TemplateView

from cases.services import get_good


class Good(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        good_pk = str(kwargs['good_pk'])
        good, _ = get_good(request, good_pk)

        context = {
            'case.id': case_id,
            'good': good['good']
        }
        return render(request, 'cases/case/good.html', context)
