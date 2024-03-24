from django.apps import AppConfig


class ProfportalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ProfPortal'
    def ready(self) :
        import ProfPortal.signals