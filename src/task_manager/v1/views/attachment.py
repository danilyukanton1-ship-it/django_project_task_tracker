from rest_framework.views import APIView
from rest_framework.response import Response
from task_manager.v1.serializers import AttachmentSerializer
from task_manager.models import Attachments
from drf_spectacular.utils import extend_schema
from django.http import Http404
from rest_framework import status


@extend_schema(tags=["Attachment"])
class AttachmentAPIView(APIView):

    def get(self, request, format=None):
        attachments = Attachments.objects.all().select_related("task")
        serializer = AttachmentSerializer(attachments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AttachmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Attachment"])
class AttachmentDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Attachments.objects.get(pk=pk)
        except Attachments.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        attachment = self.get_object(pk)
        serializer = AttachmentSerializer(attachment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        attachment = self.get_object(pk)
        serializer = AttachmentSerializer(instance=attachment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        attachment = self.get_object(pk)
        attachment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
