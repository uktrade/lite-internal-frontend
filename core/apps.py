import json

from django.apps import AppConfig

from core import strings


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        with open('lite_content/lite-internal-frontend/strings.json') as json_file:
            strings.constants = json.load(json_file)
