from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager


class User(AbstractUser):
    """Кастомная модель пользователя."""

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
