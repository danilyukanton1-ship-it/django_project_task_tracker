from rest_framework import serializers
from task_manager.models import Comments


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    priority = serializers.IntegerField()
    status = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ("id", "message", "user", "task")
