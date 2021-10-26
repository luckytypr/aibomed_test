from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


def list_users(*, filters=None):
    users = User.objects.all()
    return users


def get_user(*, user_id: str):
    user = get_object_or_404(User, id=user_id)
    return user
