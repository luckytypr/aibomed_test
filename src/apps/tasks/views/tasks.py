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

from apps.tasks.models import Task
from apps.tasks.selectors import list_tasks, get_task
from apps.tasks.services import create_task, send_executor_task_creation_info, update_task, update_task_status, \
    send_executor_task_update_info


class TaskListApi(APIView):
    api_description = _('List of tasks')

    class OutputSerializer(serializers.ModelSerializer):
        executor = inline_serializer(fields={
            'id': serializers.UUIDField(),
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'patronymic': serializers.CharField(),
        })
        observers = inline_serializer(many=True, fields={
            'id': serializers.UUIDField(),
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'patronymic': serializers.CharField(),
        })
        class Meta:
            ref_name = 'TaskListOutputSerializer'
            model = Task
            fields = (
                'id', 'name', 'executor',
                'status', 'observers',
                'created_at'
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
        tasks = list_tasks()
        return get_paginated_response(
            pagination_class=LimitOffsetPagination,
            serializer_class=self.OutputSerializer,
            queryset=tasks,
            request=request,
            view=self
        )


class TaskCreateApi(APIView):
    api_description = _('New task creation')

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        executor_id = serializers.UUIDField()
        observers = serializers.ListField(child=serializers.UUIDField())
        deadline_at = serializers.DateTimeField()
        class Meta:
            ref_name = "TaskCreateInputSerializer"


    @swagger_auto_schema(
        operation_description=api_description,
        request_body=InputSerializer
    )
    def post(self, request):
        data = request.data
        serializer = self.InputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        name = validated_data['name']
        executor_id = validated_data['executor_id']
        observers = validated_data['observers']
        deadline_at = validated_data['deadline_at']
        executor = get_user(user_id=executor_id)
        if executor_id in observers:
            raise ValidationError(
                _("You can not assign executor as observer")
            )
        task = create_task(
            name=name, executor=executor,
            observers=observers, deadline_at=deadline_at
        )
        # send_executor_task_info(user=executor, task_name=task.name)
        send_executor_task_creation_info(task=task)
        return Response(status=status.HTTP_201_CREATED)


class TaskUpdateApi(APIView):
    api_description = _('Task update')

    class InputSerializer(serializers.Serializer):
        status = serializers.CharField()
        class Meta:
            ref_name = "TaskUpdateInputSerializer"


    @swagger_auto_schema(
        operation_description=api_description,
        request_body=InputSerializer
    )
    def post(self, request, task_id):
        data = request.data
        serializer = self.InputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        task = get_task(task_id=task_id)
        task_status = validated_data.pop('status', None)
        if validated_data:
            update_task(task=task, **validated_data)
        task.refresh_from_db()
        if task_status:
            formatter = request.user
            update_task_status(
                task=task,
                new_status=task_status,
                formatter=formatter
            )
            send_executor_task_update_info(task=task)
        # send_executor_task_info(user=executor, task_name=task.name)
        # send_executor_task_info(task=task)
        return Response(status=status.HTTP_201_CREATED)