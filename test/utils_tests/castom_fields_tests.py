import pytest

from collectings.models import Payment
from src.utils.castom_fields import (get_count_amount_collect,
                                     get_count_amount_organization,
                                     get_count_donaters_collect)


@pytest.mark.django_db
def test_get_count_amount_collect(payments: list[Payment]) -> None:
    """Тест получения собранной суммы сбора."""
    collect = payments[0].collect
    assert get_count_amount_collect(collect) == 2500


@pytest.mark.django_db
def test_get_count_donaters_collect(payments: list[Payment]) -> None:
    """Тест получения количество пожертвований сбора."""
    collect = payments[0].collect
    assert get_count_donaters_collect(collect) == 5


@pytest.mark.django_db
def test_get_count_amount_organization(payments: list[Payment]) -> None:
    """Тест получения собранной суммы организации."""
    organization = payments[0].collect.organization
    assert get_count_amount_organization(organization) == 12500
