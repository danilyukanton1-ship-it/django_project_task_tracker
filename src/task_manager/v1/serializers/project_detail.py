from rest_framework import serializers
from task_manager.models import ProjectDetails


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    owner = UserSerializer(read_only=True)


class ProjectDetailsSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = ProjectDetails
        fields = ("id", "info", "serial_id", "project")
