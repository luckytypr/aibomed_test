from datetime import datetime
from apps.taskapp.celery import app
from apps.tasks.models import Task
from apps.tasks.services import send_executor_task_expired_info


@app.task(bind=True, max_retries=3)
def notify_on_task_expiration_task(self):
    now = datetime.now()
    expired_tasks = Task.objects.filter(
        deadline_at__date=now.date(),
        deadline_at__hour=now.hour,
        deadline_at__minute=now.minute,
    )
    for task in expired_tasks:
        send_executor_task_expired_info(task=task)

