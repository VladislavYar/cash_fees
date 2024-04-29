from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timedelta
from os import mkdir, path
from random import choice, randint, sample

import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import localtime
from PIL import Image, ImageDraw

from collectings.constants import (MAX_PAYMENT_AMOUNT, MAX_REQUIRED_AMOUNT,
                                   MIN_PAYMENT_AMOUNT, MIN_REQUIRED_AMOUNT)
from collectings.models import Collect, DefaultCover, Occasion, Payment
from organizations.models import Organization, Problem, Region
from users.models import User as ClassUser

User = get_user_model()


class Command(BaseCommand):

    help = 'Добавляет тестовые данные в БД.'

    @staticmethod
    def _generate_test_image(name_file: str) -> None:
        """Генерирует тестовое изображение."""
        save_dir = path.join(settings.MEDIA_ROOT, 'test_images')
        if not path.isdir(save_dir):
            mkdir(save_dir)
        width, height = 50, 50
        image = Image.new('RGB', (width, height), 'black')
        draw = ImageDraw.Draw(image)

        for _ in range(100):
            x = randint(0, width - 1)
            y = randint(0, height - 1)
            color = (
                randint(0, 255), randint(0, 255), randint(0, 255)
            )
            draw.point((x, y), fill=color)
        image.save(path.join(save_dir, name_file))

    @staticmethod
    def _create_users() -> list[ClassUser]:
        """Создаёт тестовых пользователей."""
        users = []
        password = make_password('test')
        for i in range(1, 1000):
            users.append(
                User(
                    email=f'test_{i}@test.test',
                    password=password,
                    )
                )
        return User.objects.bulk_create(users)

    @staticmethod
    def _create_regions() -> list[Region]:
        """Создаёт тестовые регионы."""
        regions = []
        for i in range(1, 51):
            regions.append(Region(name=f'Тестовый регион №{i}'))
        return Region.objects.bulk_create(regions)

    @staticmethod
    def _create_problems() -> list[Problem]:
        """Создаёт тестовые решаемые проблемы."""
        problems = []
        for i in range(1, 51):
            problems.append(
                Problem(name=f'Тестовая решаемая проблема №{i}')
                )
        return Problem.objects.bulk_create(problems)

    @staticmethod
    def _create_occasions() -> list[Occasion]:
        """Создаёт тестовые поводы."""
        occasions = []
        for i in range(1, 51):
            occasions.append(Occasion(name=f'Тестовый повод №{i}'))
        return Occasion.objects.bulk_create(occasions)

    @staticmethod
    def _create_default_covers() -> list[DefaultCover]:
        """Создаёт тестовые дефолтные обложки."""
        default_covers = []
        for i in range(1, 11):
            file_name = f'default_cover_image_test_{i}.png'
            Command._generate_test_image(file_name)
            default_covers.append(
                DefaultCover(
                    name=f'Тестовая дефолтная обложка №{i}',
                    default_cover=f'test_images/{file_name}',
                    )
                )
        return DefaultCover.objects.bulk_create(default_covers)

    @staticmethod
    def _get_full_file_name_image(
            i: int, rand_bool: tuple[bool]
            ) -> str | None:
        """Отдаёт полный адрес файла от папки media."""
        if choice(rand_bool):
            file_name_image = f'collect_image_image_test_{i}.png'
            Command._generate_test_image(file_name_image)
            return 'test_images/' + file_name_image

    @staticmethod
    def _generate_test_covers(range_collect: range) -> list[str]:
        """Генерирует тестовые обложки."""
        full_file_name_covers = []
        for i in range_collect:
            file_name_cover = f'collect_cover_image_test_{i}.png'
            Command._generate_test_image(file_name_cover)
            full_file_name_covers.append('test_images/' + file_name_cover)
        return full_file_name_covers

    @staticmethod
    def _generate_test_images(
        range_collect: range, rand_bool: tuple[bool]
            ) -> list[str]:
        """Генерирует тестовые изображения."""
        full_file_name_images = []
        for i in range_collect:
            full_file_name_images.append(
                Command._get_full_file_name_image(i, rand_bool)
            )
        return full_file_name_images

    def _create_organizations(
            self, problems: list[Problem], regions: list[Region]
            ) -> Organization:
        """Создаёт тестовые некоммерческие организации."""
        organizations = []
        for i in range(1, 51):
            file_name = f'organization_image_test_{i}.png'
            Command._generate_test_image(file_name)
            organization = Organization(
                    name=f'Тестовая некоммерческая организация №{i}',
                    cover=f'test_images/{file_name}',
                    description=(
                        f'Тестовое описание некоммерческой организации №{i}'
                        )
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
            self, local_datetime: datetime, rand_bool: tuple[bool]
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
            self, close_datetime: datetime | None,
            local_datetime: datetime,
            rand_bool: bool
            ) -> bool:
        """Отдаёт флаг активности сбора."""
        if not close_datetime:
            return not choice(rand_bool)
        return close_datetime.date() > local_datetime.date()

    def _get_covers_images(
            self, range_collect: range,
            rand_bool: tuple[bool],
            ) -> tuple[list[str]]:
        """Отдаёт обложки и изображения."""
        with ProcessPoolExecutor(
            max_workers=2, initializer=django.setup
        ) as executor:
            full_file_name_covers = executor.submit(
                Command._generate_test_covers, range_collect
                )
            full_file_name_images = executor.submit(
                Command._generate_test_images, range_collect, rand_bool)
            full_file_name_covers = full_file_name_covers.result()
            full_file_name_images = full_file_name_images.result()
        return full_file_name_covers, full_file_name_images

    def _create_collectings(
            self,
            users: list[ClassUser],
            organizations: list[Organization],
            occasions: list[Occasion],
            rand_bool: tuple[bool],
         ) -> list[Collect]:
        """Создаёт тестовые сборы."""
        collectings = []
        local_datetime = localtime()
        range_collect = range(1, 3001)

        full_file_name_covers, full_file_name_images = self._get_covers_images(
            range_collect, rand_bool
            )

        for i in range_collect:
            required_amount = randint(
                MIN_REQUIRED_AMOUNT, MAX_REQUIRED_AMOUNT+1
                )
            create_datetime, close_datetime = self._get_create_close_datetime(
                local_datetime,
                rand_bool,
                )
            is_active = self._get_is_active(
                close_datetime,
                local_datetime,
                rand_bool,
                )
            collectings.append(
                Collect(
                    user=choice(users),
                    user_first_name=f'Тестовое имя №{i}',
                    user_last_name=f'Тестовая фамилия №{i}',
                    name=f'Тестовый групповой денежный сбор №{i}',
                    organization=choice(organizations),
                    cover=full_file_name_covers[i - 1],
                    image=full_file_name_images[i - 1],
                    url_video=(
                        'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
                        if choice(rand_bool) else None
                        ),
                    description=(
                        f'Тестовое описание сбора №{i}'
                    ),
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
            self, users: list[ClassUser],
            collectings: list[Collect],
            rand_bool: tuple[bool],
            ) -> list[Payment]:
        """Создаёт тестовые платежи."""
        payments = []
        for i in range(1, 10001):
            payments.append(
                Payment(
                    user=choice(users),
                    user_first_name=f'Тестовое имя №{i}',
                    user_last_name=f'Тестовая фамилия №{i}',
                    collect=choice(collectings),
                    comment=(
                        f'Тестовый комментарий №{i}'
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
        with ProcessPoolExecutor(
            max_workers=5, initializer=django.setup
        ) as executor:
            users = executor.submit(Command._create_users)
            regions = executor.submit(Command._create_regions)
            problems = executor.submit(Command._create_problems)
            occasions = executor.submit(Command._create_occasions)
            default_covers = executor.submit(Command._create_default_covers)
            users = users.result()
            regions = regions.result()
            problems = problems.result()
            occasions = occasions.result()
            default_covers.result()
        organizations = self._create_organizations(problems, regions)
        collectings = self._create_collectings(
            users, organizations, occasions, rand_bool
            )
        self._create_payments(users, collectings, rand_bool)
