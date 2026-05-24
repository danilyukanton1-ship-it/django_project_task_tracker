from task_manager.models import UniqueQueue


class UniqueQueueService:
    def __init__(self, queue=None) -> None:
        if queue is not None:
            self.queue = queue
        else:
            self.queue = []

    def add_to_queue(self, item):
        if item not in self.queue:
            self.queue.append(item)

    def get_length(self):
        return len(self.queue)

    def get_last_item(self):
        if len(self.queue) > 0:
            return self.queue[-1]
        return None
