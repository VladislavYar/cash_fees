from django.utils.translation import gettext_lazy as _
from rest_framework.pagination import LimitOffsetPagination


class BasePagination(LimitOffsetPagination):
    """Базовый класс пагинации."""

    limit_query_description = _(
        'Количество результатов, возвращаемых на страницу.'
        )
    offset_query_description = _(
        'Начальный индекс, по которому будут выводиться результаты.'
        )
    max_limit = 20
    default_limit = 20


class OrganizationPagination(BasePagination):
    """Limit offset некоммерческих организаций."""


class CollectPagination(BasePagination):
    """Limit offset групповых денежных сборов."""
