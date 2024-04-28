import django_filters
from django.db.models import F, Sum
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

from collectings.models import Collect, Occasion
from core.models import BaseModel
from organizations.models import Organization, Problem, Region


class BaseOrderingFilter(django_filters.OrderingFilter):
    """Базовый класс сортировки."""

    def _annotate_count_amount(
            self, query: str, qs: QuerySet, values: list
    ) -> QuerySet:
        """Просчитывает общее количество пожертвований."""
        count_amount = ('count_amount', '-count_amount')
        if values and any(value in count_amount for value in values):
            return qs.annotate(count_amount=Sum(F(query)))
        return qs


class CollectOrderingFilter(BaseOrderingFilter):
    """Кастомная сортировка группового денежного сбора."""

    def filter(self, qs: QuerySet, values: list) -> QuerySet:
        qs = self._annotate_count_amount(
            'payments__payment_amount', qs, values
            )
        return super().filter(qs, values)


class OrganizationOrderingFilter(BaseOrderingFilter):
    """Кастомная сортировка некоммерческих организаций"""

    def filter(self, qs: QuerySet, values: list) -> QuerySet:
        qs = self._annotate_count_amount(
            'collectings__payments__payment_amount', qs, values
            )
        return super().filter(qs, values)


class BaseFilter(django_filters.FilterSet):
    """Базовый класс фильтра."""

    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label=BaseModel._meta.get_field('name').verbose_name,
        )

    class Meta:
        fields = ['name', 'problems']


class OrganizationFilter(BaseFilter):
    """Фильтр некоммерческих организаций."""

    problems = django_filters.ModelMultipleChoiceFilter(
        queryset=Problem.objects.all(),
        field_name='problems__slug',
        to_field_name='slug',
        label=Problem._meta.get_field('slug').verbose_name,
        )
    regions = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='regions__slug',
        to_field_name='slug',
        label=Region._meta.get_field('slug').verbose_name,
        )
    order_by = OrganizationOrderingFilter(
        fields={
            'count_amount': 'count_amount',
        },
        field_labels={
            'count_amount': _('Сумма пожертвований сборов'),
        }
    )

    class Meta(BaseFilter.Meta):
        model = Organization
        fields = BaseFilter.Meta.fields + ['regions']


class CollectFilter(BaseFilter):
    """Фильтр группового денежного сбора."""

    occasion = django_filters.CharFilter(
        field_name='occasion__slug',
        lookup_expr='exact',
        label=Occasion._meta.get_field('slug').verbose_name,
        )
    organization = django_filters.CharFilter(
        field_name='organization__slug',
        lookup_expr='exact',
        label=Organization._meta.get_field('slug').verbose_name,
        )
    region = django_filters.CharFilter(
        field_name='organization__regions__slug',
        lookup_expr='exact',
        label=Region._meta.get_field('slug').verbose_name,
        )
    problems = django_filters.ModelMultipleChoiceFilter(
        queryset=Problem.objects.all(),
        field_name='organization__problems__slug',
        to_field_name='slug',
        label=Problem._meta.get_field('slug').verbose_name,
        )
    is_active = django_filters.BooleanFilter(
        field_name='is_active',
        label=Collect._meta.get_field('is_active').verbose_name,
        )
    order_by = CollectOrderingFilter(
        fields={
            'is_active': 'is_active',
            'create_datetime': 'create_datetime',
            'count_amount': 'count_amount',
        },
        field_labels={
            'is_active': Collect._meta.get_field('is_active').verbose_name,
            'create_datetime': Collect._meta.get_field(
                'create_datetime'
                ).verbose_name,
            'count_amount': _('Сумма пожертвований сбора'),
        }
    )

    class Meta(BaseFilter.Meta):
        model = Collect
        fields = BaseFilter.Meta.fields + [
            'occasion',
            'organization',
            'region',
            'is_active',
        ]
