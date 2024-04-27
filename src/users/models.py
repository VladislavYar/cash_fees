from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.constants import MAX_LEN_PATRONYMIC
from users.managers import CustomUserManager


class User(AbstractUser):
    """Кастомная модель пользователя."""

    patronymic = models.CharField(
        max_length=MAX_LEN_PATRONYMIC,
        verbose_name=_('Отчество'),
        help_text=_('Отчество'),
        db_comment=_('Отчество'),
        blank=True,
    )
    email = models.EmailField(
        unique=True,
        verbose_name=_('Email пользователя'),
        help_text=_('Email пользователя'),
        db_comment=_('Email пользователя'),
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
    username = None
