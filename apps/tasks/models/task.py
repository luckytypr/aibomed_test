from django.db import models
from apps.common.models import TimeStampModel
from apps.tasks import TaskStatuses
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition


class Task(TimeStampModel):
    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ['-created_at']

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=126,
    )

    executor = models.ForeignKey(
        to='users.User',
        verbose_name="Исполнитель",
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    observers = models.ManyToManyField(
        to='users.User',
        verbose_name=_("Observers"),
        related_name='observing_tasks'
    )

    status = FSMField(
        verbose_name=_("Status"),
        choices=TaskStatuses.choices,
        default=TaskStatuses.PLANNING,
    )

    deadline_at = models.DateTimeField(
        verbose_name=_("Deadline"),
        help_text=_("Planning to finish at"),
    )

    @transition(
        field=status,
        source=TaskStatuses.PLANNING,
        target=TaskStatuses.ACTIVE,
    )
    def to_status_active(self):
        pass

    @transition(
        field=status,
        source=TaskStatuses.ACTIVE,
        target=TaskStatuses.CONTROLLING,
    )
    def to_status_controlling(self):
        pass

    @transition(
        field=status,
        source=TaskStatuses.CONTROLLING,
        target=TaskStatuses.FINISHED,
    )
    def to_status_finished(self):
        pass
