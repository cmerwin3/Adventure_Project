from django.apps import AppConfig
from . import models


class StoryboardConfig(AppConfig):
    name = 'storyboard'
    def ready(self):
        models.load_scripts()
