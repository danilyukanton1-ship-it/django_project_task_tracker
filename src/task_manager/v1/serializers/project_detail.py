from rest_framework.serializers import ModelSerializer
from task_manager.models import ProjectDetails


class ProjectDetailsSerializer(ModelSerializer):
    class Meta:
        model = ProjectDetails
        fields = ("info", "serial_id", "project")
