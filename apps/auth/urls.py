from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import TokenObtainPairView

app_name = "admin_authentication"

urlpatterns = [
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("access/", TokenObtainPairView.as_view(), name="access"),
]
