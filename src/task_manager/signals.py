from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from task_manager.models import Tasks, Comments, Attachments
import os
from django.core.cache import caches

cache = caches["db_cache"]


@receiver(post_save, sender=Tasks)
def create_task_created_comment(sender, instance, created, **kwargs):
    if created:
        Comments.objects.create(
            task=instance,
            message="Task created!",
        )


@receiver(post_delete, sender=Attachments)
def del_image_post_delete(sender, instance, **kwargs):
    """Удаляет фотку, после удаления записи в атачментс"""
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)


@receiver(post_save, sender=Tasks)
@receiver(post_delete, sender=Tasks)
def del_cache_post(sender, **kwargs):
    cache.clear()
