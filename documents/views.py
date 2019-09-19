from django.shortcuts import render
from django.views.generic import TemplateView


class CreateDocument(TemplateView):

    def get(self, request, **kwargs):
        context = {
            'title': 'Flags',
            'templates': [
                'eu_torture_regulation',
                'licence',
                'licence_schedule',
                'mod_letter',
                'eu_torture_regulation',
                'licence',
                'licence_schedule',
                'mod_letter',
                'eu_torture_regulation',
                'licence',
                'licence_schedule',
                'mod_letter'
            ]
        }
        return render(request, 'documents/select_a_template.html', context)


class CreateDocument2(TemplateView):

    def get(self, request, **kwargs):
        context = {
            'title': 'Flags',
        }
        return render(request, 'documents/document_generator.html', context)
