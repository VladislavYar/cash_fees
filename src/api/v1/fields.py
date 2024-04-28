import base64
import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import URLValidator
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from django_resized.forms import ResizedImageFieldFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """Класс для сериализации изображения и десериализации URI."""

    def to_internal_value(self, data: str) -> ContentFile:
        """Декодирование base64 в файл."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(";base64,")
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name=str(datetime.datetime.now().timestamp()) + "." + ext,
            )
        return super().to_internal_value(data)

    def to_representation(self, value: str | ResizedImageFieldFile) -> str:
        """Возвращает полный url изображения."""
        if value:
            uri = self.context["request"].build_absolute_uri(
                f'{settings.MEDIA_URL}{value}'
                if isinstance(value, str) else value.url
            )
            return uri


class Base64ImageOrURIField(Base64ImageField):
    """
    Класс для сериализации изображения или ссылки.

    check_model: {'model': Model, 'check_field': str}
    """
    def __init__(self, check_model: dict, **kwargs):
        """
        Добавляет данные по модели для провеки URI
        """
        self.check_model = check_model
        super().__init__(**kwargs)

    def _validate_media_uri(self, data: str) -> str:
        """Валидация ссылки на изображение."""
        uri = str.split(data, settings.MEDIA_URL, 1)
        model: Model = self.check_model['model']
        check_field = self.check_model['check_field']
        if len(uri) != 2 or not model.objects.filter(
            **{check_field: uri[1]}
        ).exists():
            raise ValidationError(_('Некорретный URI media.'))
        return uri[1]

    def to_internal_value(self, data: str) -> ContentFile | str:
        """Проверка наличия ссылки на изображение."""
        try:
            URLValidator()(data)
        except ValidationError:
            return super().to_internal_value(data)
        return self._validate_media_uri(data)
