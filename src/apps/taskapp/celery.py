import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings"
    )  # pragma: no cover

app = Celery("apps")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'notify-on-task-expiration-task': {
        'task': 'apps.tasks.tasks.notify_on_task_expiration_task',
        'schedule': crontab(),
    },
}
