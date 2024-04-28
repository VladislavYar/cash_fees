from functools import wraps

from django.db.models import Model
from rest_framework.serializers import ModelSerializer


def change_serializer_class(
        model: Model,
        serializer: ModelSerializer,
        name_field_filter: str = 'id',
):
    """Изменяет serializer для возвращаемых данных."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            request = args[0].request
            data_field_filter = response.data.get(name_field_filter)
            obj = model.objects.get(
                **{name_field_filter: data_field_filter}
                )
            response.data = serializer(
                obj,
                context={'request': request},
                ).data
            return response
        return wrapper
    return decorator
