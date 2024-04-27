from rest_framework.pagination import PageNumberPagination

from api.v1.constants import ORGANIZATION_PAGE_SIZE


class OrganizationPagination(PageNumberPagination):
    """Пагинация некоммерческих организаций."""

    page_size = ORGANIZATION_PAGE_SIZE
