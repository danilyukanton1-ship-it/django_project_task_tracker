from rest_framework import serializers
from task_manager.models import Tasks, Projects
from account.models import User


class UserTasksSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    def __init__(self, *args, **kwargs):
        """Если нужны не все поля прописываем all_fields=False и выводим только id, username и email"""
        all_fields = kwargs.pop("all_fields", True)
        super().__init__(*args, **kwargs)
        if not all_fields:
            self.fields.pop("first_name", None)
            self.fields.pop("last_name", None)


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    message = serializers.CharField()
    user = UserTasksSerializer(read_only=True, all_fields=False)


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    is_reopened = serializers.BooleanField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())
    assignee = UserTasksSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Tasks
        fields = [
            "id",
            "name",
            "description",
            "priority",
            "is_reopened",
            "status",
            "project",
            "assignee",
            "comments",
        ]
