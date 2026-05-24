import unittest
from task_manager.services import UniqueQueueService


class UniqueQueueTest(unittest.TestCase):

    def test_add_unique_item(self):
        q = UniqueQueueService()
        q.add_to_queue(1)
        self.assertEqual(q.queue, [1])
        self.assertEqual(len(q.queue), 1)

    def test_not_add_duplicate_item(self):
        q = UniqueQueueService()
        q.add_to_queue(1)
        q.add_to_queue(1)

        self.assertEqual(q.queue, [1])
        self.assertEqual(len(q.queue), 1)

    def test_add_multiple_item(self):
        q = UniqueQueueService()
        q.add_to_queue(1)
        q.add_to_queue(2)
        q.add_to_queue(3)
        self.assertEqual(q.queue, [1, 2, 3])
        self.assertEqual(len(q.queue), 3)

    def test_get_length_if_empty(self):
        q = UniqueQueueService()
        self.assertEqual(q.get_length(), 0)

    def test_get_length_after_adding_item(self):
        q = UniqueQueueService()
        q.add_to_queue(1)
        q.add_to_queue(2)
        self.assertEqual(q.get_length(), 2)

    def test_get_last_item_if_empty(self):
        q = UniqueQueueService()
        self.assertEqual(q.get_last_item(), None)

    def test_lifo_strategy(self):
        q = UniqueQueueService()
        q.add_to_queue(1)
        q.add_to_queue(2)
        q.add_to_queue(3)
        self.assertEqual(q.get_last_item(), 3)

    def test_lifo_strategy_after_duplicate_item(self):
        q = UniqueQueueService()
        q.add_to_queue(1)
        q.add_to_queue(2)
        q.add_to_queue(2)
        self.assertEqual(q.get_last_item(), 2)

    def test_init_with_existing_queue(self):
        q = UniqueQueueService([1, 2, 3])
        q.add_to_queue(4)
        self.assertEqual(q.get_last_item(), 4)
        self.assertEqual(q.get_length(), 4)


if __name__ == "__main__":
    unittest.main()
