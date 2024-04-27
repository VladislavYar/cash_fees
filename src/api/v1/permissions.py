from django.db.models import Model
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet


class IsAuthenticatedOrReadOnlyAndUpdateDeleteIsOwner(
    IsAuthenticatedOrReadOnly
):
    """
    Только аутентифицированный или только чтение.
    Удаление обновление только хозяином.
    """
    def has_object_permission(
        self, request: Request, view: ModelViewSet, obj: Model,
    ) -> bool:
        """Валидация запроса к объекту."""
        if (
            request.method not in SAFE_METHODS and
            obj.user != request.user
        ):
            return False
        return True
