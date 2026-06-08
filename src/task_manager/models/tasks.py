from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib import admin
from config.models import BaseModel


class TaskStatus(models.TextChoices):
    CREATED = "created"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELED = "canceled"
    FAILED = "failed"


class Tasks(BaseModel):
    name = models.CharField(max_length=64, unique=True, verbose_name="Наименование")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    status = models.CharField(
        choices=TaskStatus, default=TaskStatus.CREATED, verbose_name="Статус"
    )
    priority = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        verbose_name="Приоритетность",
    )
    is_reopened = models.BooleanField(default=False, verbose_name="Переоткрывалась ли")
    project = models.ForeignKey(
        to="Projects",
        related_name="tasks",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    assignee = models.ForeignKey(
        to="account.User",
        related_name="tasks",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-priority", "-created_at"]
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задача"

    def __str__(self):
        return self.name


class CompletedTaskManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status=TaskStatus.COMPLETED)


class EducationTasks(Tasks):
    objects = CompletedTaskManager()

    class Meta:
        proxy = True
