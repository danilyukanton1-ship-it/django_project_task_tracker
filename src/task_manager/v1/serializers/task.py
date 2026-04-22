from rest_framework import serializers
from task_manager.models import Tasks, Projects
from account.models import User
from task_manager.v1.serializers.comment import CommentSerializer
from django.core.cache import caches
from django.contrib.auth import get_user_model

# class TaskSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(required=True, allow_blank=False, max_length=100)
#     description = serializers.CharField(required=False, allow_blank=True, max_length=255)
#     priority = serializers.IntegerField()
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Tasks.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.name = validated_data.get("name", instance.name)
#         instance.description = validated_data.get("description", instance.description)
#         instance.priority = validated_data.get("priority", instance.priority)
#         instance.save()
#         return instance
#


class UserTasksSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()


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
