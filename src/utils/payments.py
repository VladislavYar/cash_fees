from datetime import timedelta

from django.conf import settings
from django.utils.timezone import localtime
from yookassa import Payment as YookassaPayment
from yookassa.domain.response.payment_response import PaymentResponse

from collectings.models import Collect, Payment
from utils.caching import clean_group_cache_by_tags


def create_payment(
        collect: Collect,
        collect_lookup: str,
        amount: int,
        payment_id: int,
        user_id: int
        ) -> str:
    """Создание платежа."""
    payment = YookassaPayment.create(
        {
            'amount': {
                'value': amount,
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': settings.YOOKASA_RETURN_URL,
            },
            'metadata': {
                'payment_id': payment_id,
                'collect_lookup': collect_lookup,
                'user_id': user_id,
                'collect_id': collect.id

            },
            'save_payment_method': False,
            'capture': True,
            'description': f'Пожертвование на "{collect.name}"',
        }
    )
    return payment.confirmation.confirmation_url


def clean_cache(data_clean_cache: list[dict[str, str]]) -> None:
    """Очистка кэша."""
    from api.v1.views import CollectViewSet, PaymentView
    collect_tag_cache = CollectViewSet.tag_cache
    payment_tag_cache = PaymentView.tag_cache
    tags_cache = []
    for data in data_clean_cache:
        collect_id = data['collect_id']
        lookup = data['collect_lookup']
        user_id = data['user_id']
        status = data['status']
        tags_cache.append(f'{payment_tag_cache}_queryset_{user_id}')
        if status != 'succeeded':
            continue
        organization_id = Collect.objects.get(id=collect_id).organization.id
        tags_cache.extend(
                (
                    f'{collect_tag_cache}_object_{lookup}',
                    f'{collect_tag_cache}_retrieve_{lookup}',
                    f'count_amount_collect_{collect_id}',
                    f'count_donaters_collect_{collect_id}',
                    f'count_amount_organization_{organization_id}',
                    f'{collect_tag_cache}_queryset',
                )
            )
    clean_group_cache_by_tags(set(tags_cache))


def status_payments(payments: list[PaymentResponse]) -> None:
    """Проверка статуса платежей."""
    data_clean_cache = []
    for payment in payments:
        payment_id = payment.metadata['payment_id']
        collect_lookup = payment.metadata['collect_lookup']
        user_id = payment.metadata['user_id']
        collect_id = payment.metadata['collect_id']
        payment_obj = Payment.objects.get(id=payment_id)
        if payment.status == 'waiting_for_capture':
            response = YookassaPayment.capture(payment.id)
            payment_obj.status = response.status
            payment_obj.save()
            data_clean_cache.append(
                    {
                        'collect_lookup': collect_lookup,
                        'collect_id': collect_id,
                        'user_id': user_id,
                        'status': response.status,
                    }
                )
        elif payment_obj.status != payment.status:
            payment_obj.status = payment.status
            payment_obj.save()
            data_clean_cache.append(
                    {
                        'collect_lookup': collect_lookup,
                        'collect_id': collect_id,
                        'user_id': user_id,
                        'status': payment.status,
                    }
                )
    if data_clean_cache:
        clean_cache(data_clean_cache)


def check_payments(cursor: str | None = None) -> None:
    """Проверка платежей."""
    created_at_gte = (localtime() - timedelta(minutes=30)).isoformat()
    payments = YookassaPayment.list(
                    params={
                        'created_at.gte': created_at_gte,
                        'limit': 100,
                        'cursor': cursor,
                        }
                )
    next_cursor = payments.next_cursor
    status_payments(payments.items)
    if next_cursor:
        check_payments(next_cursor)
