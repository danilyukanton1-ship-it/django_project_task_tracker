from django.core.management.base import BaseCommand
from task_manager.models import Tasks, Projects, Comments, Tags
from faker import Faker
import random
from django.contrib.auth import get_user_model
import time

fake = Faker(["en_US"])
User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        start_time = time.time()
        print("the beginning of generation!")

        print("generation of users....")
        users = []
        for i in range(100):
            user = User.objects.create_user(
                email=fake.unique.email(),
                username=fake.user_name(),
                password="123456789",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(),
            )
            users.append(user)
            if (i + 1) % 20 == 0:
                print(f"{i + 1} users already created!!!")

        print("all users already created!!")

        print("generation of projects....")
        projects = []

        for i in range(10):
            project = Projects.objects.create(
                name=fake.department_name(),
                description=fake.text(),
                owner=random.choice(users),
            )
            projects.append(project)
            print(f"{i + 1} projects already created")

        print("all projects are already created!!!")

        print("generation of tags...")
        tags = []
        for i in range(100):
            tag = Tags.objects.create(name=fake.unique.word())
            tags.append(tag)
            if (i + 1) % 20 == 0:
                print(f"{i + 1} tags already created")
        print("all tags are already created!!!")

        print("generation of tasks....")
        batch_size = 10000
        # вместо 1 запроса на 1000000 сделаем 100 запросов по 10000 чтобы не переполнять память
        # проходим циклом с шагом batch_size и на каждой итерации создаем 10000 тасков
        for i in range(0, 1000000, batch_size):
            tasks_to_create = []
            for j in range(batch_size):
                # не криэйт так как будем вставлять булком чтобы сократить кол-во запросов
                task = Tasks(
                    name=fake.unique.sentence(nb_words=3)[:64],
                    description=fake.text(),
                    status=random.choice(
                        ["created", "started", "completed", "canceled", "failed"]
                    ),
                    priority=random.randint(1, 5),
                    is_reopened=fake.boolean(),
                    project=random.choice(projects),
                    assignee=random.choice(users),
                )
                tasks_to_create.append(task)

            # вставляет в базу данных сразу 10000 объектов
            # иначе пришлось бы вставлять инсертом каждый отдельно что очень медленно при таком кол-ве
            Tasks.objects.bulk_create(tasks_to_create)
            print(f"already created {min(i + batch_size, 1000000)} tasks....")

        print("all tasks are already created!!!")

        print("adding of tags to tasks....")
        tasks = Tasks.objects.all()
        # возьмем промежуточную таблицу мэнитумэни и добавим через нее чтобы быстрее было
        through_model = Tasks.tags.through
        tag_relations = []
        processed = 0
        # берем с помощью iterator порциями чтобы не брать все 10000000000000000 обьектов сразу
        for task in tasks.iterator():
            task_tags = random.sample(tags, k=random.randint(1, 3))
            for tag in task_tags:
                tag_relations.append(through_model(tasks=task, tags=tag))

            processed += 1

            if len(tag_relations) >= 100000:
                through_model.objects.bulk_create(tag_relations, ignore_conflicts=True)
                print(f"already added tags to {processed} tasks....")
                tag_relations = []

        if tag_relations:
            through_model.objects.bulk_create(tag_relations, ignore_conflicts=True)
            print(f"already added tags to {processed} tasks....")

        print("tags are already added!!!")

        print("Generation of comments....")
        comments_to_create = []
        processed = 0
        for task in tasks.iterator():
            number_of_comms = random.randint(1, 4)
            for _ in range(number_of_comms):
                comments_to_create.append(
                    Comments(
                        task=task,
                        message=fake.unique.sentence()[:64],
                        user=random.choice(users),
                    )
                )

            processed += 1

            if len(comments_to_create) >= 100000:
                Comments.objects.bulk_create(comments_to_create)
                print(f"already created comments for {processed} tasks....")
                comments_to_create = []

        if comments_to_create:
            Comments.objects.bulk_create(comments_to_create)
            print(f"already created comments for {processed} tasks....")
        print("comments are already created")
        end_time = time.time()
        total_time = end_time - start_time
        minutes = int(total_time // 60)
        seconds = int(total_time % 60)

        print("generation was finished successfully")
        print(
            f"Total time: {minutes} minutes {seconds} seconds ({total_time:.2f} seconds)"
        )
