from random import choice

import pytest
from django.contrib.auth import get_user_model
from faker import Faker

from collectings.models import Collect, Occasion, Payment
from core.management.commands.moke_data import Command
from organizations.models import Organization, Problem, Region
from users.models import User as CastomUser

User = get_user_model()
fake = Faker('ru-RU')


@pytest.fixture
def users() -> list[CastomUser]:
    """Создание тестовых пользователей."""
    return Command.create_users(fake, 5)


@pytest.fixture
def regions() -> list[Region]:
    """Создаёт тестовые регионы."""
    return Command.create_regions(fake, 5)


@pytest.fixture
def problems() -> list[Problem]:
    """Создаёт тестовые решаемые проблемы."""
    return Command.create_problems(fake, 5)


@pytest.fixture
def occasions() -> list[Occasion]:
    """Создаёт тестовые поводы."""
    return Command.create_occasions(fake, 5)


@pytest.fixture
def organizations(problems, regions) -> list[Organization]:
    """Создание тестовых организаций."""
    return Command.create_organizations(
        problems, regions, fake, 5,
        )


@pytest.fixture
def collectings(users, organizations, occasions) -> list[Collect]:
    """Создание тестовых сборов."""
    collectings = []
    for i, organization in enumerate(organizations):
        for j, user in enumerate(users):
            collectings.append(
                Collect(
                    user=user,
                    name=f'test_name_{i}_{j}',
                    occasion=choice(occasions),
                    organization=organization,
                    )
                )
    return Collect.objects.bulk_create(collectings)


@pytest.fixture
def payments(collectings) -> list[Payment]:
    """Создание тестовых пожертвований."""
    payments = []
    len_collectings = len(collectings)
    for collect in collectings:
        for i in range(len_collectings):
            payments.append(
                Payment(
                    user=collectings[i].user,
                    collect=collect,
                    payment_amount=100,
                    )
                )
    return Payment.objects.bulk_create(payments)
