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

from apps.tasks.models import Transition
from apps.tasks.selectors import list_tasks, get_task
from apps.tasks.services import create_task, send_executor_task_creation_info, update_task


class TransitionListApi(APIView):
    api_description = _('List of task transitions')

    class OutputSerializer(serializers.ModelSerializer):
        updated_by = inline_serializer(fields={
            "id": serializers.UUIDField(),
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'patronymic': serializers.CharField(),
        })
        class Meta:
            ref_name = 'TransitionListOutputSerializer'
            model = Transition
            fields = '__all__'

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
    def get(self, request, task_id):
        task = get_task(task_id=task_id)
        transitions = task.transitions.all()
        return get_paginated_response(
            pagination_class=LimitOffsetPagination,
            serializer_class=self.OutputSerializer,
            queryset=transitions,
            request=request,
            view=self
        )
