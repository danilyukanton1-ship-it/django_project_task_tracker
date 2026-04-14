from rest_framework import serializers
from task_manager.models import Tasks, Projects
from account.models import User
from .comment import CommentSerializer


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

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    is_reopened = serializers.BooleanField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Tasks
        fields = [
            'id',
            'name',
            'description',
            'priority',
            'is_reopened',
            'status',
            'project',
            'assignee',
            'comments'
        ]
