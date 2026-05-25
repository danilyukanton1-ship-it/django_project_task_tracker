from django.test import TestCase, Client
from django.urls import reverse
from account.models import User
from task_manager.models import (
    Tasks,
    Projects,
    Attachments,
)
from task_manager.models.tasks import TaskStatus


class HomeViewTest(TestCase):
    def setUp(self):
        self.path = reverse("home")
        self.template = "tasks/home.html"

    def test_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)


class AboutViewTest(TestCase):
    def setUp(self):
        self.path = reverse("about")
        self.template = "tasks/about.html"

    def test_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)


class AddTaskViewTest(TestCase):
    def setUp(self):
        self.path = reverse("add_tasks")
        self.user = User.objects.create_user(
            username="test", email="123@test.py", password="123456"
        )
        self.project = Projects.objects.create(
            name="test",
            owner=self.user,
        )

    def test_get_request_with_template(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/add_task.html")

    def test_create_task(self):
        response = self.client.post(
            self.path,
            data={
                "name": "test",
                "description": "test",
                "project": self.project.id,
                "priority": 2,
                "status": TaskStatus.CREATED,
                "assignee": self.user.id,
            },
        )

        self.assertEqual(Tasks.objects.count(), 1)

    def test_redirect_after_creation(self):
        response = self.client.post(
            self.path,
            data={
                "name": "test",
                "description": "test",
                "project": self.project.id,
                "priority": 3,
                "status": TaskStatus.CREATED,
                "assignee": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_task_name_saved_in_session(self):
        response = self.client.post(
            self.path,
            data={
                "name": "test",
                "description": "test",
                "project": self.project.id,
                "priority": 3,
                "status": TaskStatus.CREATED,
                "assignee": self.user.id,
            },
        )
        self.assertEqual(self.client.session["pending_task_name"], "test")


class AttachmentsViewTest(TestCase):
    def setUp(self):
        self.path = reverse("attachments")
        self.user = User.objects.create_user(
            username="test", email="123@test.py", password="123456"
        )
        self.project = Projects.objects.create(
            name="test",
            owner=self.user,
        )
        self.task = Tasks.objects.create(
            name="test",
            description="test",
            project=self.project,
            priority=2,
            status=TaskStatus.CREATED,
            assignee=self.user,
        )
        self.attachment = Attachments.objects.create(
            task=self.task,
            name="test",
        )

    def test_get_request_with_template(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/attachments.html")

    def test_if_context_has_attachments(self):
        response = self.client.get(self.path)
        self.assertIn(self.attachment, response.context["attachments"])

    def test_queryset_count(self):
        response = self.client.get(self.path)
        self.assertEqual(len(response.context["attachments"]), 1)

    def test_attachment_related_task(self):
        response = self.client.get(self.path)
        attachment = response.context["attachments"][0]
        self.assertEqual(attachment.task.name, "test")


class UserTaskViewTest(TestCase):
    def setUp(self):
        self.path = reverse("user_task")
        self.user = User.objects.create_user(
            username="test",
            email="123@test.com",
            password="123456",
        )
        self.user2 = User.objects.create_user(
            username="test2",
            email="645@test.com",
            password="654321",
        )
        self.project = Projects.objects.create(
            name="test",
            owner=self.user,
        )
        self.task = Tasks.objects.create(
            name="test",
            description="test",
            project=self.project,
            priority=2,
            status=TaskStatus.CREATED,
            assignee=self.user,
        )
        self.task2 = Tasks.objects.create(
            name="test2",
            description="test2",
            project=self.project,
            priority=2,
            status=TaskStatus.CREATED,
            assignee=self.user2,
        )

    def test_get_request_with_template(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/user_task.html")

    def test_returns_only_tasks_of_current_user(self):
        response = self.client.get(self.path, {"user": self.user.email})
        tasks = response.context["tasks"]
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], self.task)
        self.assertIn(self.task, response.context["tasks"])

    def test_returns_empty_without_user_param(self):
        response = self.client.get(self.path)
        tasks = response.context["tasks"]
        self.assertEqual(len(tasks), 0)

    def test_returns_empty_if_unknown_user_param(self):
        response = self.client.get(self.path, {"user": "rererefefe@wdw.com"})
        tasks = response.context["tasks"]
        self.assertEqual(len(tasks), 0)
