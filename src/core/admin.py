from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Model, QuerySet
from django.forms import BaseFormSet, Form
from django.utils.html import format_html
from django.utils.safestring import SafeText

from core.constants import DISPLAY_IMAGE_ADMIN
from core.models import CollectOrganizationBaseModel
from utils.caching import clean_cache_by_tag


class CleanCacheAdmin(admin.ModelAdmin):
    """Очиска кэша."""

    tag_cache = None

    def save_model(
            self, request: WSGIRequest, obj: Model, form: Form, change: bool
            ) -> None:
        """Очистка кэша."""
        super().save_model(request, obj, form, change)
        clean_cache_by_tag(self.tag_cache)

    def delete_model(self, request: WSGIRequest, obj: Model) -> None:
        """Очистка кэша."""
        super().delete_model(self, request, obj)
        clean_cache_by_tag(self.tag_cache)

    def delete_queryset(
            self, request: WSGIRequest, queryset: QuerySet
            ) -> None:
        """Очистка кэша."""
        super().delete_queryset(request, queryset)
        clean_cache_by_tag(self.tag_cache)

    def save_formset(
            self, request: WSGIRequest, form: Form,
            formset: BaseFormSet, change: bool,
            ) -> None:
        """Очистка кэша."""
        super().save_formset(request, form, formset, change)
        clean_cache_by_tag(self.tag_cache)


class BaseAdmin(CleanCacheAdmin, admin.ModelAdmin):
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
        return self.list_display + ['display_cover', 'display_count_amount']

    @admin.display(
            description=CollectOrganizationBaseModel._meta.get_field(
                'cover'
                ).verbose_name
            )
    def display_cover(self, obj: Model) -> SafeText:
        """Выводит обложку в списке элементов."""
        return format_html(DISPLAY_IMAGE_ADMIN.format(obj.cover.url))


class CollectPaymentBaseAdmin(CleanCacheAdmin, admin.ModelAdmin):
    """Базовая модель админ панели сборов/платежа для сбора."""

    list_display = [
        'user',
        'user_first_name',
        'user_last_name',
    ]
