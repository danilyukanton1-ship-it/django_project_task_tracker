from django.test import TestCase, Client
from task_manager.models import Tasks
from task_manager.models.tasks import TaskStatus
from account.models import User


class TasksViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        test_user_name = "test_user"
        test_user_email = "example@gmail.com"
        test_user_password = "test"
        self.user = User.objects.create_user(
            username=test_user_name,
            email=test_user_email,
            password=test_user_password,
        )

        self.client.force_login(self.user)

    def test_task_list(self):
        test_task_name = "test_task"
        test_task_status = TaskStatus.CREATED
        test_task_priority = 1

        Tasks.objects.create(
            name=test_task_name,
            priority=test_task_priority,
            assignee=self.user,
        )

        resp = self.client.get("/tasks/")

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(Tasks.objects.count(), 1)

        obj = Tasks.objects.first()
        self.assertEqual(obj.name, test_task_name)
        self.assertEqual(obj.status, test_task_status)
        self.assertEqual(obj.priority, test_task_priority)
        self.assertEqual(obj.assignee, self.user)

    def test_create_task(self):
        path = "/tasks/add_tasks/"
        test_task_name = "test_task"
        test_priority = 2
        test_description = "test_description"
        status = TaskStatus.CREATED
        body = {
            "name": test_task_name,
            "description": test_description,
            "priority": test_priority,
            "status": status,
        }
        task = Tasks.objects.all()

        resp = self.client.post(path=path, data=body)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(task[0].name, test_task_name)
        self.assertEqual(task[0].description, test_description)
        self.assertEqual(task[0].priority, test_priority)
        self.assertEqual(task[0].status, status)
