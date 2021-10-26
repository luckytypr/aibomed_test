from django.db.models import TextChoices


class TaskStatuses(TextChoices):
    PLANNING = "PLANNING", "Планируется"
    ACTIVE = "ACTIVE", "Активная"
    CONTROLLING = "CONTROLLING", "Контроль"
    FINISHED = "FINISHED", "Завершена"
