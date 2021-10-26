from django.db import models
from django.utils.translation import gettext_lazy as _


class CheckItem(models.Model):
    class Meta:
        verbose_name = _("Checklist Item")
        verbose_name_plural = _("Checklist Items")

    task = models.ForeignKey(
        to='tasks.Task',
        verbose_name=_("Task"),
        on_delete=models.CASCADE,
        related_name="check_items"
    )

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=126,
    )

    is_done = models.BooleanField(
        verbose_name=_("Done"),
        default=False
    )
