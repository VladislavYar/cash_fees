from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import localdate

from collectings.models import Collect
from config.celery import app
from utils.payments import status_payments


@app.task
def send_mail_celery(
    subject: str, message: str, recipient_list: list
) -> None:
    """Отправляет сообщение на почту."""
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )


@app.task
def status_payments_celery() -> None:
    """Проверка статуса платежей."""
    status_payments()


@app.task
def check_close_datetime_collect() -> None:
    """
    Проверяет дату завершения сбора.
    """
    Collect.objects.filter(
        close_datetime__date__lte=localdate()
        ).update(is_active=False)
