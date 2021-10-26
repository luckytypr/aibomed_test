from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers


api_urlpatterns = [
    path('auth/', include('apps.auth.urls')),
    path('users/', include('apps.users.urls')),
]

urlpatterns = [
    path("api/", include((api_urlpatterns, 'api_urlpatterns'), namespace="api_urlpatterns")),
]

if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="Aibomed API",
            default_version='v1',
            description="Aibomed api description",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@snippets.local"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        path(
            'swagger/',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui',
        ),
    ]