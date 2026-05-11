from django.urls import path
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from account.models import User
from task_manager.models import Tasks


class TaskViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.test_password = "1234"
        self.username = "test_user"
        self.email = "test_user_email@gmail.com"
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.test_password,
        )

        self.client.force_authenticate(user=self.user)

        self.test_task_name = "test task"
        self.test_priority = 1

        self.task = Tasks.objects.create(
            name=self.test_task_name,
            priority=self.test_priority,
            assignee=self.user,
        )

    def test_create_account(self):
        path = "/api/tasks/"
        response = self.client.get(path)
        data = response.json()

        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)

        task = data["results"][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task["assignee"]["username"], self.username)
        self.assertEqual(task["assignee"]["email"], self.email)
        self.assertEqual(task["name"], self.test_task_name)
        self.assertEqual(task["priority"], self.test_priority)
