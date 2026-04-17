from task_manager.models import Attachments
from pathlib import Path
from django.core.files import File


def attachment_p_update(pk, path):
    path = Path(path)
    attachment = Attachments.objects.get(pk=pk)
    with open(path, "rb") as f:
        attachment.photo.save(name=path.name, content=File(f), save=True)
