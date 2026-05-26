from task_manager.models import UniqueQueue


class UniqueQueueService:

    @staticmethod
    def add_to_queue(item):
        if not UniqueQueue.objects.filter(item=item).exists():
            UniqueQueue.objects.create(item=item)

    @staticmethod
    def get_length():
        length = UniqueQueue.objects.count()
        return length

    @staticmethod
    def get_last_item():
        last_item = UniqueQueue.objects.order_by("-created_at").first()
        if last_item:
            return last_item.item
        return None
