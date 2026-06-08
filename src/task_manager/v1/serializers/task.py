from rest_framework import serializers
from task_manager.models import Tasks


class UserSerializer(serializers.Serializer):

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
    user = UserSerializer(read_only=True, all_fields=False)


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    owner = UserSerializer(read_only=True, all_fields=False)


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField()
    is_reopened = serializers.BooleanField()
    project = ProjectSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
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
