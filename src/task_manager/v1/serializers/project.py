from rest_framework.serializers import ModelSerializer
from task_manager.models import Projects


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ("id", "name", "description", "owner")
