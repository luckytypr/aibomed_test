from django.urls import path, include
from .views import (
    UserListApi,
    UserRegisterApi,
    MyProfileDetailApi,
)

app_name = "admin_users"

profile_urlpatterns = [
    path('', MyProfileDetailApi.as_view(), name='detail'),
]

user_patterns = [
    path('register/', UserRegisterApi.as_view(), name='register'),
    path('myprofile/', include((profile_urlpatterns, 'myprofile'))),
    path('', UserListApi.as_view(), name='list'),
]

urlpatterns = [
    path('', include((user_patterns, 'users')))
]
