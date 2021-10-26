from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.tasks import TaskStatuses


class Transition(models.Model):
    class Meta:
        verbose_name = _("Transition")
        verbose_name_plural = _("Transitions")

    task = models.ForeignKey(
        to='tasks.Task',
        verbose_name=_("Task"),
        on_delete=models.CASCADE,
        related_name="transitions"
    )

    previous_status = models.CharField(
        _('Previous Status'),
        max_length=126,
        choices=TaskStatuses.choices,
    )

    next_status = models.CharField(
        _('Next Status'),
        max_length=126,
        choices=TaskStatuses.choices,
    )

    updated_by = models.ForeignKey(
        to='users.User',
        verbose_name=_("Formatter"),
        on_delete=models.CASCADE,
        related_name="transitions"
    )
