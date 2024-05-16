from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.utils.safestring import SafeText
from django.utils.translation import gettext_lazy as _

from api.v1.views import OrganizationView, ProblemView, RegionView
from core.admin import BaseAdmin, CollectOrganizationBaseAdmin
from organizations.models import Organization, Problem, Region
from utils.castom_fields import get_count_amount_organization


@admin.register(Region)
class RegionAdmin(BaseAdmin):
    """Отображение в админ панели регионы."""

    tag_cache = RegionView.tag_cache


@admin.register(Problem)
class ProblemAdmin(BaseAdmin):
    """Отображение в админ панели решаемые проблемы."""

    tag_cache = ProblemView.tag_cache


@admin.register(Organization)
class OrganizationAdmin(CollectOrganizationBaseAdmin):
    """Отображение в админ панели некоммерческой организации."""

    list_filter = (
        'regions',
        'problems',
    )
    tag_cache = OrganizationView.tag_cache

    def get_list_display(self, request: WSGIRequest) -> list[str]:
        """Расширяет поле вывода списка элементов."""
        return super().get_list_display(request) + [
            'display_regions',
            'display_problems',
            ]

    @admin.display(description=Region._meta.verbose_name_plural)
    def display_regions(self, obj: Organization) -> SafeText:
        """Выводит регионы в списке элементов."""
        return str.join(', ', obj.regions.all().values_list('name', flat=True))

    @admin.display(description=Problem._meta.verbose_name_plural)
    def display_problems(self, obj: Organization) -> SafeText:
        """Выводит решаемые проблемы в списке элементов."""
        return str.join(
            ', ', obj.problems.all().values_list('name', flat=True)
            )

    @admin.display(
            description=_('Собранная сумма')
            )
    def display_count_amount(self, obj: Organization) -> SafeText:
        """Выводит собранную сумму."""
        return get_count_amount_organization(obj)
