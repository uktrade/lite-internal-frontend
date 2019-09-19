import os

from django.shortcuts import render
from django.template import engines
from django.views.generic import TemplateView

from conf import settings


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
            ]
        }
        return render(request, 'documents/select_a_template.html', context)


class CreateDocument2(TemplateView):

    def get(self, request, **kwargs):
        context = {
            'title': 'Flags',
        }
        return render(request, 'documents/document_generator.html', context)

    def post(self, request, **kwargs):
        django_engine = engines['django']
        template = django_engine.from_string(open(os.path.join(settings.LETTER_TEMPLATES_DIRECTORY,
                                                    'licence.html'), "r").read())
        letter_context = {
            'name': "Phil",
            'content': request.POST['content'],
            'markdown_letter_context': {'item_1': 'canon',
                                        'item_2': 'ammo',
                                        'item_3': ['tank', 'hello', 'world'],
                                        'list_of_weapons': ['tank', 'gun', 'bomb']}
        }

        preview = template.render(letter_context)

        context = {
            'title': 'Flags',
            'content': request.POST['content'],
            'preview': preview
        }
        return render(request, 'documents/document_generator.html', context)
