from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Кастомный пользовательский менеджер."""

    def create_user(
            self, email: str, password: str = None, **extra_fields
            ) -> AbstractUser:
        """Создание пользователя."""
        if not email:
            raise ValueError(_('Необходимо указать email'))
        email = self.normalize_email(email)
        user: AbstractUser = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self, email: str, password: str = None, **extra_fields
            ):
        """Создание суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is False:
            raise ValueError(
                _('У суперпользователя должно быть is_staff=True.')
                )
        if extra_fields.get('is_superuser') is False:
            raise ValueError(
                _('У суперпользователя должно быть is_superuser=True.')
                )

        return self.create_user(email, password, **extra_fields)
