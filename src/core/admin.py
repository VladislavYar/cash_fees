from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Model
from django.utils.html import format_html
from django.utils.safestring import SafeText

from core.constants import DISPLAY_IMAGE_ADMIN
from core.models import CollectOrganizationBaseModel

admin.site.unregister(Group)


class BaseAdmin(admin.ModelAdmin):
    """Базовая модель админ панели."""
    list_display = [
        'name',
        'slug',
    ]
    search_fields = [
        'name',
        'slug',
    ]
    readonly_fields = ['slug']


class CollectOrganizationBaseAdmin(BaseAdmin):
    """Базовая модель админ панели сборов/организаций."""

    def get_list_display(self, request: WSGIRequest) -> list[str]:
        """Расширяет поле вывода списка элементов."""
        return self.list_display + ['display_cover']

    @admin.display(
            description=CollectOrganizationBaseModel._meta.get_field(
                'cover'
                ).verbose_name
            )
    def display_cover(self, obj: Model) -> SafeText:
        """Выводит обложку в списке элементов."""
        return format_html(DISPLAY_IMAGE_ADMIN.format(obj.cover.url))
