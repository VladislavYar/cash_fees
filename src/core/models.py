from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from core.constants import (MAX_IMAGE_SIZE, MAX_LEN_NAME, MAX_LEN_SLUG,
                            MIN_LEN_DESCRIPTION)

User = get_user_model()


class BaseModel(models.Model):
    """Базовая модель."""

    name = models.CharField(
        max_length=MAX_LEN_NAME,
        unique=True,
        verbose_name=_('Название'),
        help_text=_('Название'),
        db_comment=_('Название'),
    )
    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        max_length=MAX_LEN_SLUG,
        unique=True,
        verbose_name=_('Slug-название'),
        help_text=_('Slug-название'),
        db_comment=_('Slug-название'),
    )

    class Meta:
        ordering = ('name',)
        abstract = True

    def __str__(self) -> str:
        return self.name


class CollectOrganizationBaseModel(BaseModel):
    """Базовая модель сборов/организаций."""

    cover = ResizedImageField(
        size=MAX_IMAGE_SIZE,
        upload_to='covers/',
        verbose_name=_('Обложка'),
        help_text=_('Обложка'),
        db_comment=_('Обложка'),
    )
    description = models.TextField(
        verbose_name=_('Описание'),
        help_text=_('Описание'),
        db_comment=_('Описание'),
        validators=(MinLengthValidator(MIN_LEN_DESCRIPTION),),
    )

    class Meta(BaseModel.Meta):
        abstract = True


class CollectPaymentBaseModel(models.Model):
    """Базовая модель сборов/платежей."""

    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        verbose_name=_('Пользователь'),
        help_text=_('Пользователь'),
        db_comment=_('Пользователь'),
        null=True,
        )
    user_first_name = models.CharField(
        max_length=User._meta.get_field('first_name').max_length,
        verbose_name=_('Имя'),
        help_text=_('Имя'),
        db_comment=_('Имя'),
        )
    user_last_name = models.CharField(
        max_length=User._meta.get_field('last_name').max_length,
        verbose_name=_('Фамилия'),
        help_text=_('Фамилия'),
        db_comment=_('Фамилия'),
    )
    create_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата и время создания'),
        help_text=_('Дата и время создания'),
        db_comment=_('Дата и время создания'),
    )

    class Meta:
        abstract = True
