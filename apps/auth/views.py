from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainPairSerializer
