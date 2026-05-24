from django.test import TestCase
from task_manager.services import UniqueQueueService
from task_manager.models import UniqueQueue


class UniqueQueueTest(TestCase):

    def test_add_unique_item(self):
        q = UniqueQueueService()
        q.add_to_queue("1")
        self.assertEqual(UniqueQueue.objects.first().item, "1")
        self.assertEqual(UniqueQueue.objects.count(), 1)

    def test_get_length(self):
        q = UniqueQueueService()
        q.add_to_queue("1")
        q.add_to_queue("2")
        q.add_to_queue("3")
        self.assertEqual(q.get_length(), UniqueQueue.objects.count())

    def test_not_add_duplicate_item(self):
        q = UniqueQueueService()
        q.add_to_queue("1")
        q.add_to_queue("1")

        self.assertEqual(UniqueQueue.objects.first().item, "1")
        self.assertEqual(q.get_length(), 1)

    def test_add_multiple_item(self):
        q = UniqueQueueService()
        q.add_to_queue("1")
        q.add_to_queue("2")
        q.add_to_queue("3")
        self.assertEqual(q.get_length(), 3)

    def test_get_length_if_empty(self):
        q = UniqueQueueService()
        self.assertEqual(q.get_length(), 0)

    def test_get_length_after_adding_item(self):
        q = UniqueQueueService()
        q.add_to_queue("1")
        q.add_to_queue("2")
        self.assertEqual(q.get_length(), 2)

    def test_get_last_item_if_empty(self):
        q = UniqueQueueService()
        self.assertEqual(q.get_last_item(), None)

    def test_lifo_strategy(self):
        q = UniqueQueueService()
        q.add_to_queue("1")
        q.add_to_queue("2")
        q.add_to_queue("3")
        self.assertEqual(q.get_last_item(), "3")

    def test_lifo_strategy_after_duplicate_item(self):
        q = UniqueQueueService()
        q.add_to_queue("1")
        q.add_to_queue("2")
        q.add_to_queue("2")
        self.assertEqual(q.get_last_item(), "2")
