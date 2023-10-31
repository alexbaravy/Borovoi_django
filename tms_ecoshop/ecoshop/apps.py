from django.apps import AppConfig


class EcoshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecoshop'
    verbose_name = "Eco Shop"

# from django.utils.translation import ugettext_lazy as _
#
# class ProfilesConfig(AppConfig):
#     name = 'cmdbox.profiles'
#     verbose_name = _('profiles')
#
#     def ready(self):
#         import cmdbox.profiles.signals  # noqa