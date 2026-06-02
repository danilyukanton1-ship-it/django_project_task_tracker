from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_celery_beat.models import PeriodicTask
from task_manager.v1.serializers import PeriodicTaskSerializer

@extend_schema(tags=['Periodic_task'])
class PeriodicTaskViewSet(ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer

    @action(detail=True, methods=['post'])
    def enable(self, request, pk=None):
        task = self.get_object()

        task.enabled = True
        task.save()

        return Response({'status': "task enabled successfully"})

    @action(detail=True, methods=['post'])
    def disable(self, request, pk=None):
        task = self.get_object()
        task.enabled = False
        task.save()
        return Response({'status': "task disabled successfully"})