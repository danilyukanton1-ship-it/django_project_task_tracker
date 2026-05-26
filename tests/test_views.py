import pytest
from django.urls import reverse
from account.models import User
from task_manager.models import Tasks, Projects, Attachments
from task_manager.models.tasks import TaskStatus


def test_home_view(client):
    response = client.get(reverse("home"))
    assert response.status_code == 200
    templates = [t.name for t in response.templates]
    assert "tasks/home.html" in templates


def test_about_view(client):
    response = client.get(reverse("about"))
    assert response.status_code == 200
    templates = [t.name for t in response.templates]
    assert "tasks/about.html" in templates


@pytest.mark.django_db
class TestAddTaskView:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username="test", email="123@wd.com", password="123456"
        )

    @pytest.fixture
    def project(self):
        return Projects.objects.create(
            name="test project",
        )

    @pytest.fixture
    def path(self):
        return reverse("add_tasks")

    @pytest.fixture
    def data(self):

        def _set_data(
            project,
            assignee,
            name="test",
            description="test",
            priority=2,
            status=TaskStatus.CREATED,
        ):
            return {
                "name": name,
                "description": description,
                "priority": priority,
                "assignee": assignee.id,
                "project": project.id,
                "status": status,
            }

        return _set_data

    def test_get_request_with_template(self, client, path):
        response = client.get(path)
        assert response.status_code == 200
        templates = [t.name for t in response.templates]
        assert "tasks/add_task.html" in templates

    def test_create_task(self, client, data, path, user, project):
        response = client.post(path, data(assignee=user, project=project))
        assert Tasks.objects.count() == 1
        assert response.status_code == 302

    def test_task_name_saved_in_session(self, client, data, path, user, project):
        response = client.post(path, data(assignee=user, project=project))
        assert client.session["pending_task_name"] == "test"


@pytest.mark.django_db
class TestAttachmentsView:

    @pytest.fixture
    def path(self):
        return reverse("attachments")

    @pytest.fixture(autouse=True)
    def project(self):
        return Projects.objects.create(
            name="test project",
        )

    @pytest.fixture(autouse=True)
    def user(self):
        return User.objects.create_user(
            username="test", email="test123@maiw.otg", password="123456"
        )

    @pytest.fixture(autouse=True)
    def task(self, user, project):
        return Tasks.objects.create(
            name="test",
            description="test",
            project=project,
            priority=2,
            status=TaskStatus.CREATED,
            assignee=user,
        )

    @pytest.fixture(autouse=True)
    def attachment(self, task):
        return Attachments.objects.create(
            task=task,
            name="test",
        )

    def test_get_request_with_template(self, client, path):
        response = client.get(path)
        assert response.status_code == 200
        templates = [t.name for t in response.templates]
        assert "tasks/attachments.html" in templates

    def test_if_context_has_attachments(self, client, path, attachment):
        response = client.get(path)
        assert attachment in response.context["attachments"]

    def test_queryset_count(self, client, path):
        response = client.get(path)
        assert len(response.context["attachments"]) == 1

    def test_attachments_related_task(self, client, path, attachment):
        response = client.get(path)
        assert response.context["attachments"][0].task.name == "test"


@pytest.mark.django_db
class TestUserTaskView:

    @pytest.fixture
    def path(self):
        return reverse("user_tasks")

    @pytest.fixture(autouse=True)
    def user1(self):
        return User.objects.create_user(
            username="test1", email="12312@wdwd.wd", password="123456"
        )

    @pytest.fixture(autouse=True)
    def user2(self):
        return User.objects.create_user(
            username="test2", email="1231@wfw.wd", password="654321"
        )

    @pytest.fixture(autouse=True)
    def project(self):
        return Projects.objects.create(
            name="test project",
        )

    @pytest.fixture(autouse=True)
    def task1(self, user1, project):
        return Tasks.objects.create(
            name="test1",
            description="test1",
            project=project,
            priority=2,
            status=TaskStatus.CREATED,
            assignee=user1,
        )

    @pytest.fixture(autouse=True)
    def task2(self, user2, project):
        return Tasks.objects.create(
            name="test2",
            description="test2",
            project=project,
            priority=2,
            status=TaskStatus.CREATED,
            assignee=user2,
        )

    def test_get_request_with_template(self, client, path):
        response = client.get(path)
        assert response.status_code == 200
        templates = [t.name for t in response.templates]
        assert "tasks/user_tasks.html" in templates

    def test_returns_only_tasks_of_current_user(self, client, path, user):
        response = client.get(path, {"user": user.email})
        tasks = response.context["tasks"]
        assert len(tasks) == 1
        assert tasks[0].name == "test1"

    def test_returns_empty_without_user_param(self, client, path):
        response = client.get(path)
        assert len(response.context["tasks"]) == 0

    def test_returns_empty_if_unknown_user_param(self, client, path):
        response = client.get(path, {"user": "adwdwdad@mail.com"})
        assert len(response.context["tasks"]) == 0
