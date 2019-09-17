from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class GcadminConfig(AppConfig):
    name = 'bbstest1.apps.gcadmin'
    def ready(self):
        autodiscover_modules("gcadmin")