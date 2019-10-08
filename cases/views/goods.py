from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page

from cases.forms.review_goods_clc import review_goods_clc_query_form
from cases.services import get_good, get_case
from conf.client import post


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
            return redirect(reverse_lazy('cases:case', kwargs={'pk': case_id}))

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
    case_id = None
    goods = None
    back_link = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs['pk'])
        self.goods = request.GET.getlist('items', request.GET.getlist('goods'))

        goods_postfix_url = "?"
        for pk in self.goods:
            goods_postfix_url += '&goods=' + pk

        self.back_link = reverse_lazy('cases:review_goods', kwargs={'pk': self.case_id}) + goods_postfix_url

        return super(ReviewGoodsClc, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = review_goods_clc_query_form(request, self.back_link)
        return form_page(request, form)

    def post(self, request, *args, **kwargs):

        form_data = {
            'objects': self.goods,
            'comment': request.POST.get('comment'),
            'report_summary': request.POST.get('report_summary'),
            'control_code': request.POST.get('control_code', None)
        }

        if request.POST.get('is_good_controlled') == 'yes':
            form_data['is_good_controlled'] = True
        elif request.POST.get('is_good_controlled') == 'no':
            form_data['is_good_controlled'] = False

        response = post(request, '/goods/controlcode/', form_data)

        if response.status_code == 400:
            form = review_goods_clc_query_form(request, self.back_link)
            return form_page(request, form, data=form_data, errors=response.json().get('errors'))

        return redirect(self.back_link)
