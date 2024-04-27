from rest_framework.pagination import PageNumberPagination

from api.v1.constants import COLLECT_PAGE_SIZE, ORGANIZATION_PAGE_SIZE


class OrganizationPagination(PageNumberPagination):
    """Пагинация некоммерческих организаций."""

    page_size = ORGANIZATION_PAGE_SIZE


class CollectPagination(PageNumberPagination):
    """Пагинация групповых денежных сборов."""

    page_size = COLLECT_PAGE_SIZE
