import django_filters
from django.shortcuts import get_object_or_404
from apps.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ('name', 'executor', 'status')


def list_tasks(*, filters=None):
    filters = filters or {}
    tasks = Task.objects.all()
    return TaskFilter(filters, tasks).qs


def get_task(*, task_id):
    task = get_object_or_404(Task, id=task_id)
    return task


def get_task_check_item(*, task: Task, item_id):
    items = task.check_items.all()
    item = get_object_or_404(items, id=item_id)
    return item
