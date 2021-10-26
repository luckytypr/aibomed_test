from celery import chain
from apps.email import send_email_task
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from django.db.utils import IntegrityError

User = get_user_model()


def create_user(*, email, password1, password2, **kwargs):
    if password1 != password2:
        raise ValidationError("Passwords don't match")
    try:
        user = User(email=email, **kwargs)
        user.set_password(password1)
        user.save()
    except IntegrityError:
        raise ValidationError(f"User with email:{email} already taken.")

    return user


def send_hello_world_to_user(*, user: User):
    send_email_task.delay(
            email=user.email,
            subject="Hello World Nandeska!",
            text="Itakakimaaaas!"
    )
