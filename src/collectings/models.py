from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from collectings.constants import (MAX_PAYMENT_AMOUNT, MAX_REQUIRED_AMOUNT,
                                   MIN_PAYMENT_AMOUNT, MIN_REQUIRED_AMOUNT,
                                   STATUSES)
from core.constants import MAX_IMAGE_SIZE
from core.models import (BaseModel, CollectOrganizationBaseModel,
                         CollectPaymentBaseModel)
from organizations.models import Organization
from utils.models import max_len_status


class Occasion(BaseModel):
    """Модель повода для сбора."""

    class Meta(BaseModel.Meta):
        verbose_name = _('Повод для сбора')
        verbose_name_plural = _('Поводы для сбора')


class DefaultCover(BaseModel):
    """Модель дефолтной обложки."""

    default_cover = ResizedImageField(
        size=MAX_IMAGE_SIZE,
        upload_to='default_cover/',
        verbose_name=_('Дефолтная обложка'),
        help_text=_('Дефолтная обложка'),
        db_comment=_('Дефолтная обложка'),
    )

    class Meta(BaseModel.Meta):
        verbose_name = _('Дефолтная обложка')
        verbose_name_plural = _('Дефолтные обложки')


class Collect(CollectOrganizationBaseModel, CollectPaymentBaseModel):
    """Модель группового денежного сбора."""

    organization = models.ForeignKey(
        to=Organization,
        on_delete=models.PROTECT,
        related_name='collectings',
        verbose_name=_('Некоммерческая организация'),
        help_text=_('Некоммерческая организация'),
        db_comment=_('Некоммерческая организация'),
        )
    occasion = models.ForeignKey(
        to=Occasion,
        on_delete=models.PROTECT,
        verbose_name=_('Повод для сбора'),
        help_text=_('Повод для сбора'),
        db_comment=_('Повод для сбора'),
        )
    image = ResizedImageField(
        size=MAX_IMAGE_SIZE,
        upload_to='images/',
        verbose_name=_('Изображение'),
        help_text=_('Изображение'),
        db_comment=_('Изображение'),
        null=True,
        blank=True,
        )
    is_active = models.BooleanField(
        verbose_name=_('Активность сбора'),
        help_text=_('Активность сбора'),
        db_comment=_('Активность сбора'),
        default=True,
        )
    url_video = models.URLField(
        verbose_name=_('URL видео'),
        help_text=_('URL видео'),
        db_comment=_('URL видео'),
        null=True,
        blank=True,
        )
    close_datetime = models.DateTimeField(
        verbose_name=_('Дата и время закрытия'),
        help_text=_('Дата и время закрытия'),
        db_comment=_('Дата и время закрытия'),
        null=True,
        blank=True,
        )
    required_amount = models.PositiveIntegerField(
        verbose_name=_('Необходимая сумма'),
        help_text=_('Необходимая сумма'),
        db_comment=_('Необходимая сумма'),
        validators=(
            MinValueValidator(MIN_REQUIRED_AMOUNT),
            MaxValueValidator(MAX_REQUIRED_AMOUNT),
            ),
        null=True,
        blank=True,
        )

    class Meta(CollectOrganizationBaseModel.Meta):
        verbose_name = _('Групповой сбор')
        verbose_name_plural = _('Групповые сборы')


class Payment(CollectPaymentBaseModel):
    """Модель платежа для сбора."""

    collect = models.ForeignKey(
        to=Collect,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name=_('Сбор'),
        help_text=_('Сбор'),
        db_comment=_('Сбор'),
        )
    comment = models.TextField(
        verbose_name=_('Комментарий'),
        help_text=_('Комментарий'),
        db_comment=_('Комментарий'),
        null=True,
        blank=True,
        )
    payment_amount = models.PositiveIntegerField(
        verbose_name=_('Сумма платежа'),
        help_text=_('Сумма платежа'),
        db_comment=_('Сумма платежа'),
        validators=(
            MinValueValidator(MIN_PAYMENT_AMOUNT),
            MaxValueValidator(MAX_PAYMENT_AMOUNT),
            )
    )
    status = models.CharField(
        max_length=max_len_status(STATUSES),
        default=STATUSES[0][0],
        choices=STATUSES,
        verbose_name=_('Статус платежа'),
        help_text=_('Статус платежа'),
        db_comment=_('Статус платежа'),
    )

    class Meta:
        verbose_name = _('Платёж')
        verbose_name_plural = _('Платежи')
