from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Model
from django.utils.html import format_html
from django.utils.safestring import SafeText

from collectings.models import Collect, DefaultCover, Occasion, Payment
from core.admin import BaseAdmin, CollectOrganizationBaseAdmin
from core.constants import DISPLAY_IMAGE_ADMIN
from organizations.constants import DISPLAY_VIDEO_ADMIN


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
    def display_default_cover(self, obj: Model) -> SafeText:
        """Выводит дефолтную обложку в списке элементов."""
        return format_html(DISPLAY_IMAGE_ADMIN.format(obj.default_cover.url))


@admin.register(Collect)
class CollectAdmin(CollectOrganizationBaseAdmin):
    """Отображение в админ панели группового денежного сбора."""

    list_filter = (
        'organization__name',
        'occasion__name',
    )

    def get_list_display(self, request: WSGIRequest) -> list[str]:
        """Расширяет поле вывода списка элементов."""
        return super().get_list_display(request) + [
            'display_image',
            'display_video',
            'user',
            ]

    @admin.display(
            description=Collect._meta.get_field(
                'image'
                ).verbose_name
            )
    def display_image(self, obj: Model) -> SafeText:
        """Выводит изображение в списке элементов."""
        if obj.image:
            return format_html(DISPLAY_IMAGE_ADMIN.format(obj.image.url))

    @admin.display(
            description=Collect._meta.get_field(
                'image'
                ).verbose_name
            )
    def display_video(self, obj: Model) -> SafeText:
        """Выводит видео в списке элементов."""
        if obj.url_video:
            uri_player = obj.url_video.replace('watch?v=', 'embed/')
            return format_html(DISPLAY_VIDEO_ADMIN.format(uri_player))


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Отображение в админ панели платежа для сбора."""

    list_filter = (
        'collect__name',
        'user__username',
        )

    list_display = (
        'user',
        'comment',
        'collect',
        'payment_amount',
    )
    search_fields = (
        'user__username',
        'collect__name',
    )
