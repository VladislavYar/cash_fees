from datetime import datetime
from urllib.parse import parse_qs, urlparse

from django.db.models import Model
from django.utils.timezone import localdate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from youtube_urls_validator import validate_url
from youtube_urls_validator.utils.exceptions import (
    HostNotInPossibleHostsError, InvalidSchemeError)

from api.v1.fields import Base64ImageField, Base64ImageOrSlugField
from collectings.models import Collect, DefaultCover, Occasion, Payment
from organizations.models import Organization, Problem, Region
from utils.castom_fields import (get_count_amount_collect,
                                 get_count_amount_organization,
                                 get_count_donaters_collect)


class BaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор."""

    class Meta:
        fields = [
            'name',
            'slug',
        ]
        read_only_fields = ['slug',]


class CollectOrganizationBaseSerializer(BaseSerializer):
    """
    Базовый сериализатор групповых денежных сборов/некоммерческих организаций.
    """

    class Meta(BaseSerializer.Meta):
        fields = BaseSerializer.Meta.fields + [
            'name',
            'slug',
            'description',
            'cover',
        ]


class CollectPaymentBaseSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор групповых денежных сборов/платежей для сбора.
    """

    class Meta:
        fields = [
            'user_first_name',
            'user_last_name',
            'create_datetime',
            ]

    def create(self, validated_data: dict) -> Model:
        """Добавляет поле с пользователем."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OccasionSerializer(BaseSerializer):
    """Сериализатор поводов сбора."""

    class Meta(BaseSerializer.Meta):
        model = Occasion


class DefaultCoverSerializer(serializers.ModelSerializer):
    """Сериализатор дефолтных обложек."""

    class Meta:
        fields = ('slug', 'default_cover',)
        model = DefaultCover


class ProblemSerializer(BaseSerializer):
    """Сериализатор решаемых проблем."""

    class Meta(BaseSerializer.Meta):
        model = Problem


class RegionSerializer(BaseSerializer):
    """Сериализатор списка регионов."""

    class Meta(BaseSerializer.Meta):
        model = Region


class OrganizationSerializer(CollectOrganizationBaseSerializer):
    """Сериализатор некоммерческих организаций."""

    count_amount = serializers.SerializerMethodField()

    class Meta(CollectOrganizationBaseSerializer.Meta):
        model = Organization
        fields = CollectOrganizationBaseSerializer.Meta.fields + [
            'count_amount',
        ]

    def get_count_amount(self, obj: Organization) -> int | None:
        """Собранная сумма."""
        return get_count_amount_organization(obj)


class PaymentSerializer(CollectPaymentBaseSerializer):
    """Сериализатор платежей для сбора."""

    collect = serializers.SlugRelatedField(
        queryset=Collect.objects.all(),
        slug_field='slug',
        )

    class Meta(CollectPaymentBaseSerializer.Meta):
        model = Payment
        fields = CollectPaymentBaseSerializer.Meta.fields + [
            'collect',
            'comment',
            'payment_amount',
            'status',
        ]
        read_only_fields = ('status',)

    def validate_collect(self, value: Collect) -> Collect:
        if not value.is_active:
            raise serializers.ValidationError(
                _('Групповой денежный сбор завершён.')
            )
        return value


class CollectUpdateSerializer(
    CollectOrganizationBaseSerializer,
    CollectPaymentBaseSerializer,
):
    """Сериализатор обновления групповых денежных сборов."""

    image = Base64ImageField(allow_null=True, required=False)
    cover = Base64ImageOrSlugField(
        {
            'model': DefaultCover,
            'check_field': 'slug',
            'get_field': 'default_cover',
            }
        )

    class Meta(
        CollectOrganizationBaseSerializer.Meta,
        CollectPaymentBaseSerializer.Meta,
    ):
        model = Collect
        fields = (
            CollectOrganizationBaseSerializer.Meta.fields +
            CollectPaymentBaseSerializer.Meta.fields + [
                'image',
                'url_video',
                'required_amount',
                'close_datetime',
            ]
        )

    def validate_close_datetime(self, value: datetime) -> datetime:
        """Валидация даты закрытия сбора."""
        if value and value.date() <= localdate():
            raise serializers.ValidationError(
                _('Дата окончания должна быть больше текушей даты.')
            )
        return value

    def _validate_param_v(self, value: str) -> str:
        """Валидация параметра v url видео."""
        parsed_url = urlparse(value)
        v = parse_qs(parsed_url.query).get('v')
        if not v:
            raise serializers.ValidationError(
                _('Некорректная ссылка на видео.')
            )
        return v[0]

    def validate_url_video(self, value: str) -> str:
        """Валидация url на видео youtube."""
        if value is None:
            return
        try:
            v = self._validate_param_v(value)
            value = f'{validate_url(value)}?v={v}'
        except (InvalidSchemeError, HostNotInPossibleHostsError):
            raise serializers.ValidationError(
                _('Некорректная ссылка на видео.')
            )
        return value


class CollectCreateSerializer(
    CollectUpdateSerializer
):
    """Сериализатор создания групповых денежных сборов."""

    organization = serializers.SlugRelatedField(
        queryset=Organization.objects.all(),
        slug_field='slug',
        )
    occasion = serializers.SlugRelatedField(
        queryset=Occasion.objects.all(),
        slug_field='slug',
        )
    count_amount = serializers.SerializerMethodField()
    count_donaters = serializers.SerializerMethodField()

    class Meta(CollectUpdateSerializer.Meta):
        fields = (
            CollectUpdateSerializer.Meta.fields + [
                'organization',
                'occasion',
                'count_amount',
                'count_donaters',
            ]
        )

    def get_count_amount(self, obj: Collect) -> int | None:
        """Собранная сумма."""
        return get_count_amount_collect(obj)

    def get_count_donaters(self, obj: Collect) -> int:
        """Количество пожертвований."""
        return get_count_donaters_collect(obj)


class CollectResponseSerializer(
    CollectCreateSerializer
):
    """Сериализатор вывода групповых денежных сборов."""

    organization = OrganizationSerializer()
    occasion = OccasionSerializer()
    payments = PaymentSerializer(many=True)

    class Meta(CollectCreateSerializer.Meta):
        fields = (
            CollectCreateSerializer.Meta.fields + [
                'is_active',
                'payments',
            ]
        )


class ConfirmationUrlSerializer(serializers.Serializer):
    """Сериализатор ссылки на оплату."""

    confirmation_url = serializers.URLField()

    class Meta:
        fields = ('confirmation_url',)
