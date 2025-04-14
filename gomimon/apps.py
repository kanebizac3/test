from django.apps import AppConfig


class GomimonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gomimon'

    def ready(self):
        import gomimon.signals