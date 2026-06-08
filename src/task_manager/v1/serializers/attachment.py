from rest_framework import serializers
from task_manager.models import Attachments


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    priority = serializers.IntegerField()
    status = serializers.CharField()


class AttachmentSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Attachments
        fields = ("id", "task", "photo")
