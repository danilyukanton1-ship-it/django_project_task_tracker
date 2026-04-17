from django.core.management.base import BaseCommand, CommandError
from task_manager.models import Tasks
from faker import Faker

fake = Faker(["en_US"])


class Command(BaseCommand):
    def handle(self, *args, **options):
        tasks = []
        try:
            for _ in range(10):
                tasks.append(Tasks(name=fake.text(max_nb_chars=30)))
            Tasks.objects.bulk_create(tasks)
            self.style.SUCCESS("Successfully created tasks")
        except Exception as e:
            self.style.ERROR(f"error is {e}")
