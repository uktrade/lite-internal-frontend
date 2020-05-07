from django.urls import reverse

from cases import services
from cases.forms.create_ecju_query import new_ecju_query_form
from cases.services import get_case, post_ecju_query
from lite_forms.views import MultiFormView


def get_ecju_queries(request, case_id):
    ecju_queries = services.get_ecju_queries(request, case_id)[0]
    open_ecju_queries = list()
    closed_ecju_queries = list()
    for query in ecju_queries.get("ecju_queries"):
        if query.get("response"):
            closed_ecju_queries.append(query)
        else:
            open_ecju_queries.append(query)
    return open_ecju_queries, closed_ecju_queries


class NewECJUQueryView(MultiFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.additional_context = {"case": get_case(request, self.object_pk)}
        self.forms = new_ecju_query_form(request, **kwargs)
        self.action = post_ecju_query
        self.success_message = "ECJU query sent successfully"
        self.success_url = reverse(
            "cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk, "tab": "ecju-queries"}
        )
