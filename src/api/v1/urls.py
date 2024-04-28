from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from api.v1.views import (CastomTokenObtainPairView, CastomUserViewSet,
                          CollectViewSet, DefaultCoverView, OccasionView,
                          OrganizationView, PaymentView, ProblemView,
                          RegionView)

app_name = 'v1'

router = routers.SimpleRouter()
router.register(r'collectings', CollectViewSet)

urlpatterns = (
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'docs/', SpectacularSwaggerView.as_view(url_name='api:v1:schema'),
        name='docs',
        ),
    path('payments/', PaymentView.as_view(), name='payments'),
    path('occansions/', OccasionView.as_view(), name='occansions'),
    path('organizations/', OrganizationView.as_view(), name='organizations'),
    path('regions/', RegionView.as_view(), name='regions'),
    path('problems/', ProblemView.as_view(), name='problems'),
    path('default-covers/', DefaultCoverView.as_view(), name='default-covers'),
    path(
        'users/', CastomUserViewSet.as_view({'post': 'create'}), name='users'
        ),
    path(
        'jwt/create/', CastomTokenObtainPairView.as_view(), name='jwt-create'
        ),
)
