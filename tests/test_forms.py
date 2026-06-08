import pytest

from account.models import User
from task_manager.forms import TasksCreationForm, CommentForm
from task_manager.models import Projects
from task_manager.models.tasks import TaskStatus


@pytest.mark.django_db
class TestTasksCreationForm:

    @pytest.fixture
    def form_factory(self):

        def _add_data_to_form(data):
            form = TasksCreationForm(data=data)

            return form

        return _add_data_to_form

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username="test",
            email="user@test.com",
            password="123456",
        )

    @pytest.fixture
    def project(self):
        return Projects.objects.create(
            name="test project",
        )

    @pytest.fixture
    def task_data(self):

        def set_data(
            user,
            project,
            name="test",
            priority=2,
            description="test description",
            status=TaskStatus.CREATED,
        ):
            return {
                "name": name,
                "priority": priority,
                "description": description,
                "status": status,
                "assignee": user.id,
                "project": project.id,
            }

        return set_data

    def test_valid_task_creation_form(self, form_factory, task_data, user, project):
        form = form_factory(task_data(user, project, 1))
        assert form.is_valid(), form.errors

    def test_priority_less_than_one(self, form_factory, task_data, user, project):
        form = form_factory(task_data(user=user, project=project, priority=-1))
        assert form.is_valid() == False, form.errors
        assert "priority" in form.errors, form.errors

    def test_priority_greater_than_five(self, form_factory, task_data, user, project):
        form = form_factory(task_data(user=user, project=project, priority=10000))
        assert form.is_valid() == False
        assert "priority" in form.errors

    def test_empty_name(self, form_factory, task_data, user, project):
        form = form_factory(task_data(user=user, project=project, name=""))
        assert form.is_valid() == False
        assert "name" in form.errors, form.errors


@pytest.mark.django_db
class TestCommentCreationForm:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username="test",
            email="test123@ukl.com",
            password="123456",
        )

    @pytest.fixture
    def form_factory(self):

        def _add_data_to_form(data):
            form = CommentForm(data=data)
            return form

        return _add_data_to_form

    @pytest.fixture
    def data(self):

        def _set_data(user, message="Test message"):
            data = {
                "message": message,
                "user": user.username if hasattr(user, "username") else user,
            }
            return data

        return _set_data

    def test_valid_task_creation_form(self, form_factory, data, user):
        form = form_factory(data(user=user.username))
        assert form.is_valid(), form.errors

    def test_invalid_user(self, form_factory, data):
        form = form_factory(data(user="test123123213"))
        assert form.is_valid() == False
        assert "user" in form.errors

    def test_empty_message(self, form_factory, data, user):
        form = form_factory(data(user=user, message=""))
        assert form.is_valid() == False
        assert "message" in form.errors

    def test_clean_user_returns_user_obj(self, form_factory, data, user):
        form = form_factory(data(user=user))
        form.is_valid()
        assert form.cleaned_data["user"] == user
