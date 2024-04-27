from rest_framework.generics import ListAPIView

from api.v1.paginations import OrganizationPagination
from api.v1.serializers import (DefaultCoverSerializer, OccasionSerializer,
                                OrganizationSerializer, ProblemSerializer,
                                RegionSerializer)
from collectings.models import DefaultCover, Occasion
from organizations.models import Organization, Problem, Region


class OccasionView(ListAPIView):
    """View вывода списка поводов сбора."""

    queryset = Occasion.objects.all()
    serializer_class = OccasionSerializer


class DefaultCoverView(ListAPIView):
    """View вывода списка дефолтных обложек."""

    queryset = DefaultCover.objects.all()
    serializer_class = DefaultCoverSerializer


class ProblemView(ListAPIView):
    """View вывода списка решаемых проблем."""

    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class RegionView(ListAPIView):
    """View вывода списка регионов."""

    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class OrganizationView(ListAPIView):
    """View вывода списка некоммерческих организаций."""

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class = OrganizationPagination
