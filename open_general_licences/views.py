from django.shortcuts import render
from django.views.generic import TemplateView

from core.services import get_control_list_entries
from lite_forms.helpers import convert_list_to_tree
from lite_forms.views import SummaryListFormView
from open_general_licences.forms import new_open_general_licence_forms


class ListView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {
            "open_general_licences": {
                "results": [
                    {
                        "id": "123",
                        "name": "Open general export licence (military goods, software and technology)",
                        "type": {"key": "open_general_export_licence", "value": "Open General Export Licence",},
                        "control_list_entries": [{"rating": "ML1a", "text": "Stuff"}],
                        "countries": [{"id": "US", "name": "United States"}, {"id": "GB", "name": "United Kingdom"}],
                        "link": "https://www.gov.uk/government/publications/open-general-export-licence-military-goods--7",
                    }
                ]
            }
        }
        return render(request, "open_general_licences/index.html", context)


class DetailView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "open_general_licences/index.html", {})


def action(_, json):
    return json, 200


class CreateView(SummaryListFormView):
    def init(self, request, **kwargs):
        self.forms = new_open_general_licence_forms(request)
        self.action = action


class UpdateView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "open_general_licences/index.html", {})
