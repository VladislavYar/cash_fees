from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CollectOrganizationBaseModel


class Region(BaseModel):
    """Модель регионов."""

    class Meta(BaseModel.Meta):
        verbose_name = _('Регион')
        verbose_name_plural = _('Регионы')


class Problem(BaseModel):
    """Модель решаемых проблем."""

    class Meta(BaseModel.Meta):
        verbose_name = _('Решаемая проблема')
        verbose_name_plural = _('Решаемые проблемы')


class Organization(CollectOrganizationBaseModel):
    """Модель некоммерческой организации."""

    problems = models.ManyToManyField(
        to=Problem,
        verbose_name=_('Решаемые проблемы'),
        help_text=_('Решаемые проблемы'),
        )
    regions = models.ManyToManyField(
        to=Region,
        verbose_name=_('Регионы'),
        help_text=_('Регионы'),
        )

    class Meta(CollectOrganizationBaseModel.Meta):
        verbose_name = _('Некоммерческая организация')
        verbose_name_plural = _('Некоммерческие организации')
