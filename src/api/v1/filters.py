import django_filters

from organizations.models import Organization, Problem, Region


class OrganizationFilter(django_filters.FilterSet):
    """Фильтр некоммерческих организаций."""

    name = django_filters.CharFilter(lookup_expr='icontains')
    problems = django_filters.ModelMultipleChoiceFilter(
        queryset=Problem.objects.all(),
        field_name='problems__slug',
        to_field_name='slug',
        )
    regions = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='regions__slug',
        to_field_name='slug',
        )

    class Meta:
        model = Organization
        fields = ('name', 'problems', 'regions')
