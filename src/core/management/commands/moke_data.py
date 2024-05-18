import io
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timedelta
from random import choice, randint, sample

import django
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import localtime
from faker import Faker

from collectings.constants import (MAX_PAYMENT_AMOUNT, MAX_REQUIRED_AMOUNT,
                                   MIN_PAYMENT_AMOUNT, MIN_REQUIRED_AMOUNT,
                                   STATUSES)
from collectings.models import Collect, DefaultCover, Occasion, Payment
from core.constants import MAX_LEN_NAME
from organizations.models import Organization, Problem, Region
from users.models import User as CastomUser

User = get_user_model()

SIZE_IMAGE = (5, 5)


class Command(BaseCommand):

    help = 'Добавляет тестовые данные в БД.'

    @staticmethod
    def create_users(fake: Faker, count: int) -> list[CastomUser]:
        """Создаёт тестовых пользователей."""
        users = []
        password = make_password('test')
        for i in range(count):
            users.append(
                User(
                    email=fake.unique.ascii_free_email(),
                    password=password,
                    )
                )
        return User.objects.bulk_create(users)

    def _get_rand_first_last_name(self, fake: Faker) -> tuple[str]:
        """Отдаёт рандомные имя и фамилию."""
        if randint(0, 1):
            return (fake.first_name_male(), fake.last_name_male())
        return (fake.first_name_female(), fake.last_name_female())

    @staticmethod
    def _generate_test_images(
        range_collect: range,
        fake: Faker,
        tag: str,
        rand_bool: tuple[bool] | None = None,
    ) -> list[str]:
        """Генерирует тестовые изображения."""
        images = []
        for i in range_collect:
            if rand_bool and not choice(rand_bool):
                images.append(None)
                continue
            file_name_image = f'collect_{tag}_image_test_{i+1}.png'
            images.append(
                ImageFile(
                    io.BytesIO(fake.image(SIZE_IMAGE)), name=file_name_image,
                    )
                )
        return images

    @staticmethod
    def create_regions(fake: Faker, count: int) -> list[Region]:
        """Создаёт тестовые регионы."""
        regions = []
        for i in range(count):
            regions.append(Region(name=fake.unique.region()))
        return Region.objects.bulk_create(regions)

    @staticmethod
    def create_problems(fake: Faker, count: int) -> list[Problem]:
        """Создаёт тестовые решаемые проблемы."""
        problems = []
        for i in range(count):
            problems.append(
                Problem(name=fake.unique.text(max_nb_chars=MAX_LEN_NAME))
                )
        return Problem.objects.bulk_create(problems)

    @staticmethod
    def create_occasions(fake: Faker, count: int) -> list[Occasion]:
        """Создаёт тестовые поводы."""
        occasions = []
        for i in range(count):
            occasions.append(
                Occasion(name=fake.unique.text(max_nb_chars=MAX_LEN_NAME))
                )
        return Occasion.objects.bulk_create(occasions)

    @staticmethod
    def create_default_covers(fake: Faker, count: int) -> list[DefaultCover]:
        """Создаёт тестовые дефолтные обложки."""
        default_covers = []
        range_collect = range(count)
        covers = Command._generate_test_images(
            range_collect, fake, 'default_cover',
            )
        for i in range_collect:
            default_covers.append(
                DefaultCover(
                    name=fake.unique.text(max_nb_chars=MAX_LEN_NAME),
                    default_cover=covers[i],
                    )
                )
        return DefaultCover.objects.bulk_create(default_covers)

    @staticmethod
    def _get_valid_name_company(fake: Faker) -> str:
        """Отдаёт валидное название компании."""
        while True:
            name = fake.unique.company()
            if len(name) <= MAX_LEN_NAME:
                return name

    @staticmethod
    def create_organizations(
            problems: list[Problem],
            regions: list[Region],
            fake: Faker,
            count: int,
            ) -> Organization:
        """Создаёт тестовые некоммерческие организации."""
        organizations = []
        range_collect = range(count)
        covers = Command._generate_test_images(
            range_collect, fake, 'organization_cover',
            )
        for i in range_collect:
            organization = Organization(
                    name=Command._get_valid_name_company(fake),
                    cover=covers[i],
                    description=fake.text(),
                    )
            organizations.append(organization)
        organizations = Organization.objects.bulk_create(organizations)
        with transaction.atomic():
            for organization in organizations:
                organization.problems.set(
                    sample(problems, randint(0, len(problems)-1)))

                organization.regions.set(
                    sample(regions, randint(0, len(regions)-1))
                    )
                organization.save()
        return organizations

    def _get_create_close_datetime(
            self, local_datetime: datetime, rand_bool: tuple[bool],
            ) -> tuple[datetime | None]:
        """Отдаёт дату и время создания/закрытия сбора."""
        create_datetime = local_datetime - timedelta(
            days=randint(0, 61),
            hours=randint(0, 61),
            minutes=randint(0, 61),
            )
        close_datetime = None
        if not choice(rand_bool):
            close_datetime = create_datetime + timedelta(
                days=randint(1, 121),
                hours=randint(0, 121),
                minutes=randint(0, 121),
            )
        return create_datetime, close_datetime

    def _get_is_active(
            self,
            close_datetime: datetime | None,
            local_datetime: datetime,
            rand_bool: bool
            ) -> bool:
        """Отдаёт флаг активности сбора."""
        if not close_datetime:
            return not choice(rand_bool)
        return close_datetime.date() > local_datetime.date()

    def _get_covers_images(
            self,
            range_collect: range,
            rand_bool: tuple[bool],
            fake: Faker,
            ) -> tuple[list[str]]:
        """Отдаёт обложки и изображения."""
        with ProcessPoolExecutor(
            max_workers=2, initializer=django.setup
        ) as executor:
            covers = executor.submit(
                Command._generate_test_images,
                range_collect,
                fake,
                'collecting_cover',
                )
            images = executor.submit(
                Command._generate_test_images,
                range_collect,
                fake,
                'collecting_image',
                rand_bool,
                )
            covers = covers.result()
            images = images.result()
        return covers, images

    def _create_collectings(
            self,
            users: list[CastomUser],
            organizations: list[Organization],
            occasions: list[Occasion],
            rand_bool: tuple[bool],
            fake: Faker,
            count: int,
         ) -> list[Collect]:
        """Создаёт тестовые сборы."""
        collectings = []
        local_datetime = localtime()
        range_collect = range(count)
        covers, images = self._get_covers_images(
            range_collect, rand_bool, fake,
            )

        for i in range_collect:
            required_amount = randint(
                MIN_REQUIRED_AMOUNT, MAX_REQUIRED_AMOUNT+1
                )
            create_datetime, close_datetime = (
                self._get_create_close_datetime(
                    local_datetime,
                    rand_bool,
                    )
                )
            is_active = self._get_is_active(
                close_datetime, local_datetime, rand_bool,
                )
            name = self._get_rand_first_last_name(fake)
            collectings.append(
                Collect(
                    user=choice(users),
                    user_first_name=name[0],
                    user_last_name=name[1],
                    name=fake.unique.text(max_nb_chars=MAX_LEN_NAME),
                    organization=choice(organizations),
                    cover=covers[i],
                    image=images[i],
                    url_video=(
                        'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
                        if choice(rand_bool) else None
                        ),
                    description=fake.text(),
                    occasion=choice(occasions),
                    required_amount=(
                        required_amount if not choice(rand_bool) else None
                        ),
                    is_active=is_active,
                    create_datetime=create_datetime,
                    close_datetime=close_datetime,
                    )
                )
        return Collect.objects.bulk_create(collectings)

    def _create_payments(
            self, users: list[CastomUser],
            collectings: list[Collect],
            rand_bool: tuple[bool],
            fake: Faker,
            count: int,
            ) -> list[Payment]:
        """Создаёт тестовые платежи."""
        payments = []
        for i in range(count):
            name = self._get_rand_first_last_name(fake)
            payments.append(
                Payment(
                    user=choice(users),
                    user_first_name=name[0],
                    user_last_name=name[1],
                    collect=choice(collectings),
                    status=choice(STATUSES)[0],
                    comment=(
                        fake.text()
                        if not choice(rand_bool) else None
                        ),
                    payment_amount=randint(
                        MIN_PAYMENT_AMOUNT,
                        MAX_PAYMENT_AMOUNT,
                    )
                    )
                )
        return Payment.objects.bulk_create(payments)

    def handle(self, *args, **options):
        rand_bool = (True, False, False)
        fake = Faker('ru_RU')
        with ProcessPoolExecutor(
            max_workers=5, initializer=django.setup,
        ) as executor:
            users = executor.submit(Command.create_users, fake, 1000)
            regions = executor.submit(Command.create_regions, fake, 50)
            problems = executor.submit(Command.create_problems, fake, 50)
            occasions = executor.submit(Command.create_occasions, fake, 50)
            default_covers = executor.submit(
                Command.create_default_covers, fake, 10,
                )
            users = users.result()
            regions = regions.result()
            problems = problems.result()
            occasions = occasions.result()
            default_covers.result()
        organizations = Command.create_organizations(
            problems, regions, fake, 50,
            )
        collectings = self._create_collectings(
            users, organizations, occasions, rand_bool, fake, 3000,
            )
        # self._create_payments(users, collectings, rand_bool, fake, 10000)
