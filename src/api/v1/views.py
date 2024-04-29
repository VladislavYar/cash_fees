from django.core.cache import cache
from django.db.models import QuerySet
from djoser.conf import settings
from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.filters import CollectFilter, OrganizationFilter
from api.v1.paginations import CollectPagination, OrganizationPagination
from api.v1.permissions import IsAuthenticatedOrReadOnlyAndUpdateDeleteIsOwner
from api.v1.serializers import (CollectCreateSerializer,
                                CollectResponseSerializer,
                                CollectUpdateSerializer,
                                DefaultCoverSerializer, OccasionSerializer,
                                OrganizationSerializer, PaymentSerializer,
                                ProblemSerializer, RegionSerializer)
from api.v1.tasks import send_mail_celery
from collectings.models import Collect, DefaultCover, Occasion, Payment
from organizations.models import Organization, Problem, Region
from utils.caching import (CachedSetMixin, ListCachedMixin,
                           ListCreateCachedMixin, clean_cache_by_tag)
from utils.decorators import change_serializer_class


@extend_schema_view(
    create=extend_schema(
        responses={200: settings.SERIALIZERS.user},
        summary='Создание нового пользователя',
        description='Создаёт нового пользователя',
        tags=('Пользователь',),
    ),
)
class CastomUserViewSet(UserViewSet):
    """Кастомизация swagger-a."""


@extend_schema_view(
    post=extend_schema(
        responses={201: TokenObtainPairSerializer},
        summary='Получение токена',
        description='Отдаёт токен',
        tags=('Пользователь',),
    ),
)
class CastomTokenObtainPairView(TokenObtainPairView):
    """Кастомизация swagger-a."""


@extend_schema_view(
    get=extend_schema(
        responses={200: ProblemSerializer(many=True)},
        summary='Список решаемых проблем.',
        description='Выводит список решаемых проблем.',
        tags=('Некоммерческая организация',),
    ),
)
class ProblemView(ListCachedMixin, ListAPIView):
    """View вывода списка решаемых проблем."""

    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    tag_cache = 'problem'


@extend_schema_view(
    get=extend_schema(
        responses={200: RegionSerializer(many=True)},
        summary='Список регионов',
        description='Выводит список регионов',
        tags=('Некоммерческая организация',),
    ),
)
class RegionView(ListCachedMixin, ListAPIView):
    """View вывода списка регионов."""

    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    tag_cache = 'region'


@extend_schema_view(
    get=extend_schema(
        responses={200: OrganizationSerializer(many=True)},
        summary='Список некоммерческих организаций',
        description='Выводит список некоммерческих организаций',
        tags=('Некоммерческая организация',),
    ),
)
class OrganizationView(ListCachedMixin, ListAPIView):
    """View вывода списка некоммерческих организаций."""

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class = OrganizationPagination
    filterset_class = OrganizationFilter
    tag_cache = 'organization'


@extend_schema_view(
    get=extend_schema(
        responses={200: OccasionSerializer(many=True)},
        summary='Список поводов сбора',
        description='Выводит список поводов сбора',
        tags=('Групповой денежный сбор',),
    ),
)
class OccasionView(ListCachedMixin, ListAPIView):
    """View вывода списка поводов сбора."""

    queryset = Occasion.objects.all()
    serializer_class = OccasionSerializer
    tag_cache = 'occasions'


@extend_schema_view(
    get=extend_schema(
        responses={200: DefaultCoverSerializer(many=True)},
        summary='Список дефолтных обложек',
        description='Выводит список дефолтных обложек',
        tags=('Групповой денежный сбор',),
    ),
)
class DefaultCoverView(ListCachedMixin, ListAPIView):
    """View вывода списка дефолтных обложек."""

    queryset = DefaultCover.objects.all()
    serializer_class = DefaultCoverSerializer
    tag_cache = 'default_cover'


@extend_schema_view(
    list=extend_schema(
        responses={200: CollectResponseSerializer(many=True)},
        summary='Список групповых денежных сборов',
        description='Выводит список групповых денежных сборов',
        tags=('Групповой денежный сбор',),
    ),
    retrieve=extend_schema(
        responses={200: CollectResponseSerializer()},
        summary='Получить групповой денежный сбор',
        description='Отдаёт групповой денежный сбор',
        tags=('Групповой денежный сбор',),
    ),
    create=extend_schema(
        responses={201: CollectResponseSerializer()},
        summary='Создать групповой денежный сбор',
        description='Создаёт групповой денежный сбор',
        tags=('Групповой денежный сбор',),
    ),
    update=extend_schema(
        responses={200: CollectResponseSerializer()},
        summary='Обновить групповой денежный сбор',
        description='Обновляет групповой денежный сбор',
        tags=('Групповой денежный сбор',),
    ),
    partial_update=extend_schema(
        responses={200: CollectResponseSerializer()},
        summary='Обновить групповой денежный сбор',
        description='Обновляет групповой денежный сбор',
        tags=('Групповой денежный сбор',),
    ),
    destroy=extend_schema(
        responses={204: None},
        summary='Сделать неактивным групповой денежный сбор',
        description='Делает неактивным групповой денежный сбор',
        tags=('Групповой денежный сбор',),
    ),
)
class CollectViewSet(CachedSetMixin, ModelViewSet):
    """View вывода списка групповых денежных сборов."""

    queryset = Collect.objects.all()
    serializer_class = CollectResponseSerializer
    pagination_class = CollectPagination
    filterset_class = CollectFilter
    permission_classes = (
        IsAuthenticatedOrReadOnlyAndUpdateDeleteIsOwner,
        )
    lookup_field = 'slug'
    tag_cache = 'collect'

    def get_serializer_class(self, *args, **kwargs) -> ModelSerializer:
        """Изменяет сериализатор в зависимости от запроса."""
        serializer_class = self.serializer_class
        method = self.request.method
        if method in ('PUT', 'PATCH'):
            serializer_class = CollectUpdateSerializer
        elif method == 'POST':
            serializer_class = CollectCreateSerializer
        return serializer_class

    @change_serializer_class(
        model=Collect,
        serializer=CollectResponseSerializer,
        name_field_filter='slug',
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменяет сериализатор вывода и создаёт task на отправку сообщения.
        """
        response = super().create(request, *args, **kwargs)
        send_mail_celery.delay(
            'Create collect',
            f'Групповой денежный сбор "{response.data['name']}" создан.',
            (request.user.email,)
        )
        return response

    @change_serializer_class(
        model=Collect,
        serializer=CollectResponseSerializer,
        name_field_filter='slug',
    )
    def update(self, request: Request, *args, **kwargs) -> Response:
        """Изменяет сериализатор вывода."""
        return super().update(request, *args, **kwargs)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Делает групповой денежный сбор неактивным."""
        instance: Collect = self.get_object()
        instance.is_active = False
        instance.save()
        clean_cache_by_tag(self.tag_cache)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(
        responses={200: PaymentSerializer(many=True)},
        summary='Список личных платежей для сбора',
        description='Выводит список личных платежей для сбора',
        tags=('Групповой денежный сбор',),
    ),
    post=extend_schema(
        responses={201: PaymentSerializer(many=True)},
        summary='Создать платёж для сбора',
        description='Создаёт платеже для сбора',
        tags=('Групповой денежный сбор',),
    )
)
class PaymentView(ListCreateCachedMixin, ListCreateAPIView):
    """View вывода платежей для сбора."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)
    tag_cache = 'payment'

    def get_queryset(self) -> QuerySet[Payment]:
        """Отдаёт платежи для сбора пользователя и кэширует данные."""
        queryset = cache.get(f'{self.tag_cache}_queryset')
        if not queryset:
            queryset = self.queryset.filter(user=self.request.user)
            cache.set(f'{self.tag_cache}_queryset', queryset)
        return queryset

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Cоздаёт task на отправку сообщения и очищает кэш по сборам."""
        response = super().create(request, *args, **kwargs)
        clean_cache_by_tag(CollectViewSet.tag_cache)
        send_mail_celery.delay(
            'Create payment',
            'Платеж для сбора создан.',
            (request.user.email,)
        )
        return response
