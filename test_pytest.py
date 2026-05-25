from src.task_manager.services import UniqueQueueService
from src.task_manager.models import UniqueQueue
import pytest


@pytest.mark.parametrize(["item", "res"], [("1", "1"), (1, "1")])
@pytest.mark.django_db
def test_unique_queue(item, res):
    q = UniqueQueueService()
    q.add_to_queue(item)
    assert UniqueQueue.objects.first().item == res


@pytest.mark.parametrize(
    ["item1", "item2", "item3", "res"], [("1", "2", "3", "3"), (1, 2, 3, "3")]
)
@pytest.mark.django_db
def test_add__multiple_to_queue(item1, item2, item3, res):
    q = UniqueQueueService()
    q.add_to_queue(item1)
    q.add_to_queue(item2)
    q.add_to_queue(item3)
    assert UniqueQueue.objects.all().count() == 3
    assert UniqueQueue.objects.order_by("-created_at").first().item == res
