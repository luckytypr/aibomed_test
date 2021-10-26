from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.selectors import (
    list_users,
)
from apps.common.pagination import get_paginated_response, LimitOffsetPagination
from apps.common.swagger_params import (
    limit_params,
    offset_params,
)
from apps.users.services import create_user

from django.contrib.auth import get_user_model

User = get_user_model()


class UserListApi(APIView):
    api_description = _('List of users')

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            ref_name = 'UserListOutputSerializer'
            model = User
            fields = (
                'id', 'email', 'first_name',
                'last_name', 'patronymic',
                'last_login'
            )

    @swagger_auto_schema(
        operation_description=api_description,
        manual_parameters=[
            limit_params,
            offset_params,
        ],
        responses={
            status.HTTP_200_OK: OutputSerializer(many=True)
        }
    )
    def get(self, request):
        users = list_users()
        return get_paginated_response(
            pagination_class=LimitOffsetPagination,
            serializer_class=self.OutputSerializer,
            queryset=users,
            request=request,
            view=self
        )


class MyProfileDetailApi(APIView):
    api_description = _('My profile details information')

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            ref_name = 'MyProfileDetailOutputSerializer'
            model = User
            exclude = ('password', )

    @swagger_auto_schema(
        operation_description=api_description,
        responses={
            status.HTTP_200_OK: OutputSerializer()
        }
    )
    def get(self, request):
        user = request.user
        serializer = self.OutputSerializer(user)
        return Response(serializer.data)


class UserRegisterApi(APIView):
    api_description = _('New user registration')

    class InputSerializer(serializers.ModelSerializer):
        username_field = User.USERNAME_FIELD

        password1 = serializers.CharField(max_length=128, min_length=8, required=False,)
        password2 = serializers.CharField(max_length=128, min_length=8, required=False,)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields[self.username_field] = serializers.CharField()

        class Meta:
            ref_name = "UserRegisterInputSerializer"
            model = User
            fields = (
                'first_name',
                'last_name',
                'patronymic',
                'email',
                'password1',
                'password2',
            )

    @swagger_auto_schema(
        operation_description=api_description,
        request_body=InputSerializer
    )
    def post(self, request):
        data = request.data
        serializer = self.InputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        email = validated_data.pop('email')
        password1 = validated_data.pop('password1', None)
        password2 = validated_data.pop('password2', None)
        create_user(
            email=email, password1=password1,
            password2=password2, **validated_data
        )
        return Response(status=status.HTTP_201_CREATED)
