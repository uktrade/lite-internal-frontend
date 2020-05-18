from django.shortcuts import render
from django.views.generic import TemplateView


class ListView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {
            "open_general_licences": {
                "results": [
                    {
                        "id": "123",
                        "name": "Open general export licence (military goods, software and technology)",
                        "type": {
                            "key": "open_general_export_licence",
                            "value": "Open General Export Licence",
                        },
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


class CreateView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "open_general_licences/index.html", {})


class UpdateView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "open_general_licences/index.html", {})
