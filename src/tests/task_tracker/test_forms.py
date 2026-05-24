from django.test import TestCase

from account.models import User
from task_manager.forms import TasksCreationForm, CommentForm
from task_manager.models import Projects
from task_manager.models.tasks import TaskStatus


class TasksCreationFormTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="test",
            email="user@test.com",
            password="123456",
        )

        self.project = Projects.objects.create(
            name="Test Project",
        )

    def test_valid_task_creation_form(self):
        form = TasksCreationForm(
            data={
                "name": "Test task",
                "priority": 3,
                "description": "Test description",
                "status": TaskStatus.CREATED,
                "assignee": self.user.id,
                "project": self.project.id,
            }
        )
        self.assertTrue(form.is_valid())

    def test_priority_less_than_one(self):
        form = TasksCreationForm(
            data={
                "name": "Test task",
                "priority": 0,
                "description": "Test description",
                "status": TaskStatus.CREATED,
                "assignee": self.user.id,
                "project": self.project.id,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("priority", form.errors)

    def test_priority_greater_than_five(self):
        form = TasksCreationForm(
            data={
                "name": "Test task",
                "priority": 6,
                "description": "Test description",
                "status": TaskStatus.CREATED,
                "assignee": self.user.id,
                "project": self.project.id,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("priority", form.errors)

    def test_empty_name(self):
        form = TasksCreationForm(
            data={
                "name": "",
                "priority": 3,
                "description": "Test description",
                "status": TaskStatus.CREATED,
                "assignee": self.user.id,
                "project": self.project.id,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class CommentsCreationFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            email="test@test.com",
            password="123456",
        )

    def test_valid_task_creation_form(self):
        form = CommentForm(
            data={
                "user": self.user.username,
                "message": "Test message",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_user(self):
        form = CommentForm(
            data={
                "user": "test1231231",
                "message": "Test message",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("user", form.errors)

    def test_empty_message(self):
        form = CommentForm(
            data={
                "user": self.user.username,
                "message": "",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_clean_user_returns_user_object(self):
        form = CommentForm(
            data={
                "user": self.user.username,
                "message": "Test message",
            }
        )
        form.is_valid()
        self.assertEqual(form.cleaned_data["user"], self.user)
