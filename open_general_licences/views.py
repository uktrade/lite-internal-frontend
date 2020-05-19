from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from lite_forms.views import SummaryListFormView
from open_general_licences.forms import new_open_general_licence_forms


class ListView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {
            "open_general_licences": {
                "results": [
                    {
                        "id": "00000000-0000-0000-0000-000000000001",
                        "name": "military goods, software and technology",
                        "description": "This OGEL allows, subject to certain conditions, the export of military goods to certain destinations if they have been temporarily imported into the UK for exhibition or demonstration purposes only.Exporters must register with the Export Control Organisation before they make use of most OGELs. All Open General Licences remain in force until they are revoked.",
                        "type": {"key": "open_general_export_licence", "value": "Open general export licence",},
                        "control_list_entries": [{"rating": "ML1a", "text": "Stuff"}],
                        "countries": [{"id": "US", "name": "United States"}, {"id": "GB", "name": "United Kingdom"}],
                        "link": "https://www.gov.uk/government/publications/open-general-export-licence-military-goods--7",
                    }
                ]
            }
        }
        return render(request, "open-general-licences/index.html", context)


class DetailView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {
            "open_general_licence":
                {
                    "id": "00000000-0000-0000-0000-000000000001",
                    "name": "military goods, software and technology",
                    "description": "This OGEL allows, subject to certain conditions, the export of military goods to certain destinations if they have been temporarily imported into the UK for exhibition or demonstration purposes only.Exporters must register with the Export Control Organisation before they make use of most OGELs. All Open General Licences remain in force until they are revoked.",
                    "type": {"key": "open_general_export_licence", "value": "Open general export licence", },
                    "control_list_entries": [{"rating": "ML1a", "text": "Stuff"}],
                    "countries": [{"id": "US", "name": "United States"}, {"id": "GB", "name": "United Kingdom"}],
                    "link": "https://www.gov.uk/government/publications/open-general-export-licence-military-goods--7",
                    "status": {"value": "Deactivated"}
                }
        }
        return render(request, "open-general-licences/open-general-licence.html", context)


def action(_, json):
    return json, 200


class CreateView(SummaryListFormView):
    def init(self, request, **kwargs):
        self.forms = new_open_general_licence_forms(request)
        self.action = action
        self.summary_list_title = "Confirm details about this licence"
        self.summary_list_button = "Submit"
        self.summary_list_notice_title = None
        self.summary_list_notice_text = None
        self.hide_titles = True
        self.success_message = "OGL added successfully"
        self.success_url = reverse("open_general_licences:open_general_licences")


class UpdateView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "open_general_licences/index.html", {})
