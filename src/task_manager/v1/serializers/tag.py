from task_manager.models import Tags
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    tasks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tags
        fields = ("id", "name", "tasks_count")
