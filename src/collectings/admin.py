from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Model, QuerySet
from django.forms import BaseFormSet, Form
from django.utils.html import format_html
from django.utils.safestring import SafeText
from django.utils.translation import gettext_lazy as _

from api.v1.views import (CollectViewSet, DefaultCoverView, OccasionView,
                          PaymentView)
from collectings.constants import DISPLAY_VIDEO_ADMIN
from collectings.models import Collect, DefaultCover, Occasion, Payment
from core.admin import (BaseAdmin, CollectOrganizationBaseAdmin,
                        CollectPaymentBaseAdmin)
from core.constants import DISPLAY_IMAGE_ADMIN
from utils.caching import clean_cache_by_tag
from utils.castom_fields import (get_count_amount_collect,
                                 get_count_donaters_collect)


@admin.register(Occasion)
class OccasionAdmin(BaseAdmin):
    """Отображение в админ панели повода для сбора."""

    tag_cache = OccasionView.tag_cache


@admin.register(DefaultCover)
class DefaultCoverAdmin(BaseAdmin):
    """Отображение в админ панели дефолтной обложки."""

    tag_cache = DefaultCoverView.tag_cache

    def get_list_display(self, request: WSGIRequest) -> list[str]:
        """Расширяет поле вывода списка элементов."""
        return super().get_list_display(request) + [
            'display_default_cover',
            ]

    @admin.display(
            description=DefaultCover._meta.get_field(
                'default_cover'
                ).verbose_name
            )
    def display_default_cover(self, obj: DefaultCover) -> SafeText:
        """Выводит дефолтную обложку в списке элементов."""
        return format_html(DISPLAY_IMAGE_ADMIN.format(obj.default_cover.url))


@admin.register(Collect)
class CollectAdmin(CollectOrganizationBaseAdmin, CollectPaymentBaseAdmin):
    """Отображение в админ панели группового денежного сбора."""

    tag_cache = CollectViewSet.tag_cache

    list_filter = (
        'organization__name',
        'occasion__name',
        'is_active',
    )

    def get_list_display(self, request: WSGIRequest) -> list[str]:
        """Расширяет поле вывода списка элементов."""
        return (
            CollectPaymentBaseAdmin.list_display +
            super().get_list_display(request) + [
                'display_count_donaters',
                'display_image',
                'display_video',
                'is_active',
            ]
        )

    @admin.display(
            description=Collect._meta.get_field(
                'image'
                ).verbose_name
            )
    def display_image(self, obj: Collect) -> SafeText:
        """Выводит изображение в списке элементов."""
        if obj.image:
            return format_html(DISPLAY_IMAGE_ADMIN.format(obj.image.url))

    @admin.display(
            description=Collect._meta.get_field(
                'url_video'
                ).verbose_name
            )
    def display_video(self, obj: Collect) -> SafeText:
        """Выводит видео в списке элементов."""
        if obj.url_video:
            uri_player = obj.url_video.replace('watch?v=', 'embed/')
            return format_html(DISPLAY_VIDEO_ADMIN.format(uri_player))

    @admin.display(
            description=_('Собранная сумма')
            )
    def display_count_amount(self, obj: Collect) -> SafeText:
        """Выводит собранную сумму."""
        return get_count_amount_collect(obj)

    @admin.display(
            description=_('Количество пожертвований')
            )
    def display_count_donaters(self, obj: Collect) -> SafeText:
        """Выводит количество пожертвований."""
        return get_count_donaters_collect(obj)


@admin.register(Payment)
class PaymentAdmin(CollectPaymentBaseAdmin):
    """Отображение в админ панели платежа для сбора."""

    list_filter = (
        'status',
        'collect__name',
        'user__email',
        )

    search_fields = (
        'user__email',
        'collect__name',
    )

    tag_cache = PaymentView.tag_cache
    collect_tag_cache = CollectViewSet.tag_cache

    def get_list_display(self, request: WSGIRequest) -> list[str]:
        """Расширяет поле вывода списка элементов."""
        return super().get_list_display(request) + [
            'status',
            'collect',
            'payment_amount',
            'comment',
            ]

    def save_model(
            self, request: WSGIRequest, obj: Model, form: Form, change: bool
            ) -> None:
        """Очистка кэша сборов."""
        super().save_model(request, obj, form, change)
        clean_cache_by_tag(self.collect_tag_cache)

    def delete_model(self, request: WSGIRequest, obj: Model) -> None:
        """Очистка кэша сборов."""
        super().delete_model(self, request, obj)
        clean_cache_by_tag(self.collect_tag_cache)

    def delete_queryset(
            self, request: WSGIRequest, queryset: QuerySet
            ) -> None:
        """Очистка кэша сборов."""
        super().delete_queryset(request, queryset)
        clean_cache_by_tag(self.collect_tag_cache)

    def save_formset(
            self, request: WSGIRequest, form: Form,
            formset: BaseFormSet, change: bool,
            ) -> None:
        """Очистка кэша сборов."""
        super().save_formset(request, form, formset, change)
        clean_cache_by_tag(self.collect_tag_cache)
