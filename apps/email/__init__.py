from apps.taskapp.celery import app

from .tasks import BaseEmailSenderTask

send_email_task = app.register_task(BaseEmailSenderTask())
