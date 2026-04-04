from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tasks, Comments


@receiver(post_save, sender=Tasks)
def create_task_created_comment(sender, instance, created, **kwargs):
    if created:
        Comments.objects.create(
            task=instance,
            message='Task created!',
        )
