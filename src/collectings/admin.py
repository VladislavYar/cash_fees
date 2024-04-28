from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.utils.html import format_html
from django.utils.safestring import SafeText

from collectings.constants import DISPLAY_VIDEO_ADMIN
from collectings.models import Collect, DefaultCover, Occasion, Payment
from core.admin import (BaseAdmin, CollectOrganizationBaseAdmin,
                        CollectPaymentBaseAdmin)
from core.constants import DISPLAY_IMAGE_ADMIN


@admin.register(Occasion)
class OccasionAdmin(BaseAdmin):
    """Отображение в админ панели повода для сбора."""


@admin.register(DefaultCover)
class DefaultCoverAdmin(BaseAdmin):
    """Отображение в админ панели дефолтной обложки."""

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
                'image'
                ).verbose_name
            )
    def display_video(self, obj: Collect) -> SafeText:
        """Выводит видео в списке элементов."""
        if obj.url_video:
            uri_player = obj.url_video.replace('watch?v=', 'embed/')
            return format_html(DISPLAY_VIDEO_ADMIN.format(uri_player))


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

    def get_list_display(self, request: WSGIRequest) -> list[str]:
        """Расширяет поле вывода списка элементов."""
        return super().get_list_display(request) + [
            'status',
            'collect',
            'payment_amount',
            'comment',
            ]
