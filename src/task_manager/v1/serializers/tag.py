from task_manager.models import Tags
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from task_manager.models import Tasks


class TagSerializer(ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tasks.objects.all().prefetch_related("tasks")
    )

    class Meta:
        model = Tags
        fields = ("id", "name", "tasks")
