from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()
fake = Faker('en_US')


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("the beginning of generation!")

        print('generation of users....')
        users = []
        for i in range(100):
            user = User.objects.create_user(
                email=fake.unique.email(),
                username=fake.user_name(),
                password='123456789',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number()
            )
            users.append(user)
            if (i + 1) % 20 == 0:
                print(f'{i + 1} users already created!!!')

        print('all users already created!!')
