from django.db import models


from config.models import BaseModel


class Attachments(BaseModel):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name = "Наименование"
    )

    task = models.ForeignKey(
        to="Tasks",
        on_delete=models.CASCADE,
        related_name="attachments"
    )

    class Meta:
        ordering = ["name"]
        db_table = "attachments"
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"

    def __str__(self):
        return self.name