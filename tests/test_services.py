from task_manager.services import UniqueQueueService
from task_manager.models import UniqueQueue
import pytest


@pytest.mark.django_db
class TestUniqueQueueService:

    @pytest.fixture
    def queue_factory(self):

        def _create_queue(items):

            queue = UniqueQueueService()

            for item in items:
                queue.add_to_queue(item)

            return queue

        return _create_queue

    @pytest.mark.parametrize(["item", "res"], [("1", "1"), (1, "1")])
    def test_if_adds_items_to_queue(self, queue_factory, item, res):
        queue = queue_factory([item])
        assert queue.get_last_item() == res

    @pytest.mark.parametrize(
        ["items", "res"], [(["1", "2", "3"], "3"), ([1, 2, 3], "3")]
    )
    def test_add_multiple_to_queue(self, queue_factory, items, res):
        queue = queue_factory(items)
        assert UniqueQueue.objects.all().count() == 3
        assert queue.get_last_item() == res

    @pytest.mark.parametrize(["item", "res"], [("1", "1"), (1, "1")])
    def test_not_to_duplicate(self, queue_factory, item, res):
        queue = queue_factory([item, item])
        assert queue.get_length() == 1
        assert queue.get_last_item() == res

    @pytest.mark.parametrize(["items"], [(["1", "2", "3"],)])
    def test_get_length(self, queue_factory, items):
        queue = queue_factory(items)
        assert queue.get_length() == 3

    @pytest.mark.parametrize(["items", "res"], [(["1", "2", "3"], "3")])
    def test_lifo_strategy(self, queue_factory, items, res):
        queue = queue_factory(items)
        assert queue.get_last_item() == res

    def test_empty_queue_returns_none(self, queue_factory):
        queue = queue_factory([])
        assert queue.get_length() == 0
        assert queue.get_last_item() is None
