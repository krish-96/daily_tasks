from django.apps import AppConfig


class DsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ds_app'

    def ready(self):
        import ds_app.signals

