from rest_framework.views import APIView
from task_manager.models import ProjectDetails
from task_manager.v1.serializers import ProjectDetailsSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Project_details"])
class ProjectDetailsAPIView(APIView):

    def get(self, request):
        projects = ProjectDetails.objects.all().select_related("project")
        serializer = ProjectDetailsSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Project_details"])
class ProjectDetailsDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return ProjectDetails.objects.get(pk=pk)
        except ProjectDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectDetailsSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectDetailsSerializer(instance=project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
