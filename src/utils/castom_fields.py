from django.core.cache import cache
from django.db.models import F, Sum

from collectings.models import Collect
from organizations.models import Organization


def get_count_amount_collect(obj: Collect) -> int | None:
    """Собранная сумма."""
    key = f'count_amount_collect_{obj.id}'
    count_amount = cache.get(key)
    if count_amount:
        return count_amount
    count_amount = obj.payments.filter(
        status='succeeded'
        ).aggregate(
        count_amount=Sum('payment_amount')
        )['count_amount']
    cache.set(key, count_amount)
    return count_amount


def get_count_donaters_collect(obj: Collect) -> int | None:
    """Количество пожертвований."""
    key = f'count_donaters_collect_{obj.id}'
    count_donaters = cache.get(key)
    if count_donaters:
        return count_donaters
    count_donaters = obj.payments.filter(
        status='succeeded'
        ).values('user').distinct().count()
    cache.set(key, count_donaters)
    return count_donaters


def get_count_amount_organization(obj: Organization) -> int | None:
    """Собранная сумма."""
    key = f'count_amount_organization_{obj.id}'
    count_amount = cache.get(key)
    if count_amount:
        return count_amount
    count_amount = obj.collectings.aggregate(
            count_amount=Sum(F('payments__payment_amount'))
        )['count_amount']
    cache.set(key, count_amount)
    return count_amount
