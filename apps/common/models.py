import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name=_("Creation Time"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name=_("Last Update Time"),
        auto_now_add=True,
    )


class UUIDModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(default=None, primary_key=True)

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):

        if self.id is None:
            self.id = uuid.uuid4()

        return super(UUIDModel, self).save(
            force_insert, force_update, using, update_fields)