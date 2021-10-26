from django.db import models
from apps.common.models import TimeStampModel, UUIDModel
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager


class User(UUIDModel,
           AbstractBaseUser,
           TimeStampModel):

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'

    email = models.EmailField(
        verbose_name=_("Email"),
        unique=True,
        db_index=True,
    )

    first_name = models.CharField(
        verbose_name=_("Firstname"),
        max_length=32,
        default="",
        db_index=True
    )

    last_name = models.CharField(
        verbose_name=_("Lastname"),
        max_length=56,
        default="",
        db_index=True
    )

    patronymic = models.CharField(
        verbose_name=_("Patronymic"),
        max_length=56,
        default="",
        blank=True,
    )
