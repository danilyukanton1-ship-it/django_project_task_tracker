from task_manager.models import Tags
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("id", "name")
