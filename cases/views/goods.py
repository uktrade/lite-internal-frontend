from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from lite_forms.generators import form_page

from cases.forms.review_goods_clc import review_goods_clc_query_form
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
    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        objects = request.GET.getlist('items', request.GET.getlist('goods'))
        goods = []
        if not objects:
            raise Http404

        case = get_case(request, case_id)

        edit_flags_url = reverse_lazy('cases:assign_flags', kwargs={'pk': case_id}) + '?level=goods&origin=review_goods'
        review_goods_clc_url = reverse_lazy('cases:review_goods_clc', kwargs={'pk': case_id})
        goods_postfix_url = ""
        for good in case['application']['goods']:
            if good['good']['id'] in objects:
                goods.append(good)
                goods_postfix_url += '&goods=' + good['good']['id']

        context = {
            'title': 'Review Goods',
            'case_id': case_id,
            'objects': goods,
            'edit_flags_url': edit_flags_url + goods_postfix_url,
            'review_goods_clc_url': review_goods_clc_url + '?' + goods_postfix_url[1:]
        }
        return render(request, 'cases/case/review-goods.html', context)


class ReviewGoodsClc(TemplateView):

    def get(self, request, **kwargs):
        case_id = str(kwargs['pk'])
        objects = request.GET.getlist('items', request.GET.getlist('goods'))

        goods_postfix_url = ""
        for pk in objects:
            goods_postfix_url += '&goods=' + pk

        back_link = reverse_lazy('cases:review_goods', kwargs={'pk': case_id}) + '?' + goods_postfix_url[1:]
        form = review_goods_clc_query_form(request, back_link)
        return form_page(request, form)
