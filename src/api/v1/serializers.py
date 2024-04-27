from rest_framework import serializers

from collectings.models import DefaultCover, Occasion
from organizations.models import Organization, Problem, Region


class BaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор."""
    class Meta:
        fields = [
            'name',
            'slug',
        ]


class OccasionSerializer(BaseSerializer):
    """Сериализатор поводов сбора."""

    class Meta(BaseSerializer.Meta):
        model = Occasion


class DefaultCoverSerializer(serializers.ModelSerializer):
    """Сериализатор дефолтных обложек."""

    class Meta:
        fields = ('default_cover',)
        model = DefaultCover


class ProblemSerializer(BaseSerializer):
    """Сериализатор решаемых проблем."""

    class Meta(BaseSerializer.Meta):
        model = Problem


class RegionSerializer(BaseSerializer):
    """Сериализатор списка регионов."""

    class Meta(BaseSerializer.Meta):
        model = Region


class OrganizationSerializer(serializers.ModelSerializer):
    """Сериализатор некоммерческих организаций."""

    class Meta:
        model = Organization
        fields = (
            'name',
            'slug',
            'description',
            'cover',
            )
