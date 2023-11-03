from django.apps import AppConfig


class EcoshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecoshop'
    verbose_name = "Eco Shop"

    def ready(self):
        import ecoshop.signals


