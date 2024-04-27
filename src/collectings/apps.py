from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CollectingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collectings'
    verbose_name = _('Групповые сборы')
