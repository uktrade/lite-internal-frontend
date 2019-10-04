from django.http import Http404
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from cases.services import get_good, get_case


class Good(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        good_pk = str(kwargs['good_pk'])
        good, _ = get_good(request, good_pk)

        context = {
            'case_id': case_id,
            'good': good['good']
        }
        return render(request, 'cases/case/good.html', context)


class ReviewGoods(TemplateView):
    # case_id = None
    # objects = None
    # # context = None
    #
    # def dispatch(self, request, *args, **kwargs):
    #     self.case_id = str(kwargs['pk'])
    #     self.objects = request.GET.getlist('items', request.GET.getlist('goods'))
    #
    #     if not self.objects:
    #         raise Http404
    #
    #     return super(ReviewGoods, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        objects = request.GET.getlist('items', request.GET.getlist('goods'))
        goods = []
        if not objects:
            raise Http404

        case = get_case(request, case_id)

        edit_flags_url = reverse_lazy('cases:assign_flags', kwargs={'pk': case_id}) + '?level=goods&origin=review_goods'

        for good in case['application']['goods']:
            if good['good']['id'] in objects:
                goods.append(good)
                edit_flags_url += '&goods=' + good['good']['id']

        context = {
            'title': 'Review Goods',
            'case_id': case_id,
            'objects': goods,
            'edit_flags_url': edit_flags_url
        }
        return render(request, 'cases/case/review-goods.html', context)


