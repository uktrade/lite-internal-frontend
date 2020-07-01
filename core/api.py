from django.http import JsonResponse
from django.views.generic import TemplateView

from queues.services import get_cases_search_data


class Cases(TemplateView):
    def get(self, request, **kwargs):
        data = get_cases_search_data(request, kwargs["pk"], {})
        # pprint(data)
        return JsonResponse(data=data)
