from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from apps.common.utils import inline_serializer
from apps.users.selectors import get_user
from apps.common.pagination import get_paginated_response, LimitOffsetPagination
from apps.common.swagger_params import (
    limit_params,
    offset_params,
)

from apps.tasks.models import CheckItem
from apps.tasks.selectors import list_tasks, get_task, get_task_check_item
from apps.tasks.services import (
    update_task_check_item,
    create_check_item
)


class CheckItemListApi(APIView):
    api_description = _('List of task check items')

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            ref_name = 'CheckItemListOutputSerializer'
            model = CheckItem
            fields = '__all__'

    @swagger_auto_schema(
        operation_description=api_description,
        responses={
            status.HTTP_200_OK: OutputSerializer(many=True)
        }
    )
    def get(self, request, task_id):
        task = get_task(task_id=task_id)
        items = task.check_items.all()
        data = self.OutputSerializer(items, many=True).data
        return Response(data)


class CheckItemCreateApi(APIView):
    api_description = _('Create task check item')

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        class Meta:
            ref_name = 'CheckItemCreateInputSerializer'

    @swagger_auto_schema(
        operation_description=api_description,
        request_body=InputSerializer
    )
    def post(self, request, task_id):
        task = get_task(task_id=task_id)

        data = request.data
        serializer = self.InputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data

        item = create_check_item(task=task, **validated_data)
        return Response(status=status.HTTP_201_CREATED)


class CheckItemUpdateApi(APIView):
    api_description = _('Update task check item')

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        is_done = serializers.BooleanField()
        class Meta:
            ref_name = 'CheckItemUpdateInputSerializer'

    @swagger_auto_schema(
        operation_description=api_description,
        request_body=InputSerializer
    )
    def post(self, request, task_id, item_id):
        task = get_task(task_id=task_id)
        item = get_task_check_item(task=task, item_id=item_id)

        data = request.data
        serializer = self.InputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data

        update_task_check_item(item=item, **validated_data)
        return Response(status=status.HTTP_200_OK)


class CheckItemDeleteApi(APIView):
    api_description = _('Delete task check item')

    @swagger_auto_schema(
        operation_description=api_description,
    )
    def post(self, request, task_id, item_id):
        task = get_task(task_id=task_id)
        item = get_task_check_item(task=task, item_id=item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
