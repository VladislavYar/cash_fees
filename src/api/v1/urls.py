from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api.v1.views import (DefaultCoverView, OccasionView, OrganizationView,
                          ProblemView, RegionView)

app_name = 'v1'


urlpatterns = (
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'docs/', SpectacularSwaggerView.as_view(url_name='api:v1:schema'),
        name='docs',
        ),
    path('occansions/', OccasionView.as_view(), name='occansions'),
    path('organizations/', OrganizationView.as_view(), name='organizations'),
    path('regions/', RegionView.as_view(), name='regions'),
    path('problems/', ProblemView.as_view(), name='problems'),
    path('default-covers/', DefaultCoverView.as_view(), name='default-covers'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
)
