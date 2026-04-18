from functools import lru_cache

from task_manager.models import Attachments
from pathlib import Path
from django.core.files import File


def attachment_p_update(pk, path):
    path = Path(path)
    attachment = Attachments.objects.get(pk=pk)
    with open(path, "rb") as f:
        attachment.photo.save(name=path.name, content=File(f), save=True)


@lru_cache(maxsize=128)
def sum_of_pos_nums(nums: tuple):
    import time

    time.sleep(1)
    if len(nums) == 0:
        return 0
    if nums[0] > 0:
        return nums[0] + sum_of_pos_nums(nums[1:])
    return sum_of_pos_nums(nums[1:])


a = (1, 1, 1, 1)
print(sum_of_pos_nums(a))
