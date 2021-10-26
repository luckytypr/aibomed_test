from typing import List
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from apps.common.utils import update_model_object
from apps.email import send_email_task
from django.contrib.auth import get_user_model
from apps.tasks.models import Task, Transition, CheckItem
from apps.tasks import TaskStatuses
User = get_user_model()


def create_task(
        *, name: str,
        executor: User,
        observers: List,
        deadline_at: str,
):
    task = Task(
        name=name,
        executor=executor,
        deadline_at=deadline_at
    )
    task.save()
    task.observers.set(observers)
    return task


def send_executor_task_creation_info(*, task: Task):
    executor = task.executor
    observers = list(task.observers.all().values_list('first_name', 'last_name', 'patronymic', 'email'))

    responsibles = "\n".join(f"{obs[3]}: {obs[0]} {obs[1]} {obs[2]}" for obs in observers)
    all_responsibles = responsibles + f"\n{executor.email}: {executor.first_name} {executor.last_name} {executor.patronymic} <- исполнитель"

    observer_emails = [obs[3] for obs in observers]

    send_email_task.delay(
            emails=executor.email,
            subject="AIBOMED",
            text=f"Задача: {task.name}\n"
                 f"Вам назначена новая задача!\n"
                 f"Наблюдатели:\n"
                 f"{responsibles}"

    )

    send_email_task.delay(
            emails=observer_emails,
            subject="AIBOMED",
            text=f"Задача: {task.name}\n"
                 f"Была назначена новая задача!\n"
                 f"Ответсвенные:\n"
                 f"{all_responsibles}"
    )


def send_executor_task_update_info(*, task: Task):
    executor = task.executor
    observers = list(task.observers.all().values_list('first_name', 'last_name', 'patronymic', 'email'))
    responsibles = "\n".join(f"{obs[3]}: {obs[0]} {obs[1]} {obs[2]}" for obs in observers)
    all_responsibles = responsibles + f"\n{executor.email}: {executor.first_name} {executor.last_name} {executor.patronymic} <- исполнитель"
    observer_emails = [obs[3] for obs in observers]

    send_email_task.delay(
            emails=executor.email,
            subject="AIBOMED",
            text=f"Задача: {task.name}\n"
                 f"Ваша задача была переведена в статус: {task.status}!\n"
                 f"Наблюдатели:\n"
                 f"{responsibles}"

    )

    send_email_task.delay(
            emails=observer_emails,
            subject="AIBOMED",
            text=f"Задача: {task.name}\n"                 
                 f"Задача была переведена в статус: {task.status}!\n"
                 f"Ответсвенные:\n"
                 f"{all_responsibles}"
    )


def create_task_transition(
        *,
        task: Task,
        previous_status: str,
        next_status: str,
        updated_by: User
):
    transition = Transition(
        task=task,
        previous_status=previous_status,
        next_status=next_status,
        updated_by=updated_by,
    )
    transition.save()
    return transition


def update_task(*, task: Task, formatter: User, **kwargs):
    update_model_object(model=task, **kwargs)


def update_task_status(*, task: Task, new_status: str, formatter: User):
    prev_status = task.status
    new_status = new_status

    if new_status == TaskStatuses.CONTROLLING.name:
        task.to_status_controlling()
    elif new_status == TaskStatuses.ACTIVE.name:
        task.to_status_active()
    elif new_status == TaskStatuses.FINISHED.name:
        task.to_status_finished()
    else:
        ValidationError(_(f"Can not change task status to unknown staus: {new_status}"))
    task.save()
    if prev_status != new_status:
        create_task_transition(
            task=task,
            previous_status=prev_status,
            next_status=new_status,
            updated_by=formatter,
        )


def send_executor_task_expired_info(*, task: Task):
    executor = task.executor
    observers = list(task.observers.all().values_list('first_name', 'last_name', 'patronymic', 'email'))
    responsibles = "\n".join(f"{obs[3]}: {obs[0]} {obs[1]} {obs[2]}" for obs in observers)

    send_email_task.delay(
            emails=executor.email,
            subject="AIBOMED",
            text=f"Задача: {task.name}\n"
                 f"Ваша задача была просрочена!\n"
                 f"Наблюдатели:\n"
                 f"{responsibles}"

    )


def create_check_item(*, task: Task, **kwargs):
    item = CheckItem(task=task, **kwargs)
    item.save()
    return item


def update_task_check_item(*, item: CheckItem, **kwargs):
    update_model_object(model=item, **kwargs)
