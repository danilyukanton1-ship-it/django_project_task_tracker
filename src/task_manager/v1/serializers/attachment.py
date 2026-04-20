from rest_framework.serializers import ModelSerializer
from task_manager.models import Attachments


class AttachmentSerializer(ModelSerializer):

    class Meta:
        model = Attachments
        fields = ("id", "task", "photo")
