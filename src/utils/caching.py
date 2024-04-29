from django.core.cache import cache
from django.db.models import Model, QuerySet
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer


def clean_cache_by_tag(tag_cache: str) -> None:
    """Очищает кэш по тегу."""
    keys = cache.keys(f'{tag_cache}_*')
    cache.delete_many(keys)


class QuerysetCachedMixin(GenericAPIView):
    """Кэширование queryset."""

    def get_queryset(self) -> QuerySet[Model]:
        """Кэширование списка данных."""
        key = f'{self.tag_cache}_queryset'
        queryset = cache.get(key)
        if not queryset:
            queryset = super().get_queryset()
            cache.set(key, queryset)
        return queryset


class ListCachedMixin(ListModelMixin):
    """Кэширование вывода списка."""

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Кэширование отфильтрованных данных."""
        key = f'{self.tag_cache}_{dict(request.GET).__str__()}'
        data = cache.get(key)
        if not data:
            response = super().list(request, *args, **kwargs)
            cache.set(key, response.data)
            return response
        return Response(data)


class ListQuerysetCachedMixin(ListCachedMixin, QuerysetCachedMixin):
    """Кэширование вывода списка и queryset."""


class ObjectCachedMixin(GenericAPIView):
    """Кеширование объекта."""

    def get_object(self) -> Model:
        """Кеширование объекта."""
        lookup = self.kwargs[self.lookup_field]
        key = f'{self.tag_cache}_object_{lookup}'
        obj = cache.get(key)
        if not obj:
            obj = super().get_object()
            cache.set(key, obj)
        return obj


class RetrieveCachedMixin(RetrieveModelMixin):
    """Кеширование вывода объекта."""

    def retrieve(
            self, request: Request, *args, **kwargs
            ) -> Response:
        """Кеширование вывода объекта."""
        lookup = self.kwargs[self.lookup_field]
        key = f'{self.tag_cache}_retrieve_{lookup}'
        data = cache.get(key)
        if not data:
            response = super().retrieve(request, *args, **kwargs)
            cache.set(key, response.data)
            return response
        return Response(data)


class RetrieveObjectCachedMixin(RetrieveCachedMixin, ObjectCachedMixin):
    """Кэширование вывода объекта и object."""


class CleanCachedMixin:
    """Очистка кэша."""

    def clean_cache(self,) -> None:
        """Очищает кэш по по тегу."""
        clean_cache_by_tag(self.tag_cache)


class CreateCachedMixin(CreateModelMixin, CleanCachedMixin):
    """Очистка кэша при создании объекта."""

    def perform_create(self, serializer: ModelSerializer) -> None:
        """Очитска кэша при создании объекта."""
        super().perform_create(serializer)
        self.clean_cache()


class UpdateCachedMixin(UpdateModelMixin, CleanCachedMixin):
    """Очистка кэша при обновлении объекта."""

    def perform_update(self, serializer: ModelSerializer) -> None:
        """Очитска кэша при изменении объекта."""
        super().perform_update(serializer)
        self.clean_cache()


class DestroyCachedMixin(DestroyModelMixin, CleanCachedMixin):
    """Очистка кэша при удалении объекта."""

    def perform_destroy(self, instance: Model) -> None:
        """Очитска кэша при удалени объекта."""
        super().perform_destroy(instance)
        self.clean_cache()


class ListCreateCachedMixin(ListCachedMixin, CreateCachedMixin):
    """Кэширование списка данных и очистка при создании."""


class CachedSetMixin(CreateCachedMixin,
                     RetrieveCachedMixin,
                     UpdateCachedMixin,
                     DestroyCachedMixin,
                     ListCachedMixin,
                     ):
    """Полный контроль кэширования."""
