from task_manager.models import Tasks
from task_manager.v1.serializers import TaskSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.core.cache import caches
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

redis_cache = caches["redis"]


@extend_schema(tags=["Task"])
class TaskAPIViewSet(ModelViewSet):
    queryset = (
        Tasks.objects.all()
        .prefetch_related("tags")
        .select_related("assignee", "project")
    )
    serializer_class = TaskSerializer

    def get_cache_key(self):
        return f'task:{self.kwargs["pk"]}'

    @extend_schema(responses={200: TaskSerializer})
    def get(self, request, *args, **kwargs):
        cache_key = self.get_cache_key()
        task = redis_cache.get(cache_key)

        if task is not None:
            return Response(task)
        else:
            task_obj = get_object_or_404(Tasks, pk=kwargs["pk"])
            serialized_task = TaskSerializer(task_obj).data
            redis_cache.set(cache_key, serialized_task, 600)
            return Response(serialized_task)

    @extend_schema(request=TaskSerializer, responses={200: TaskSerializer})
    def put(self, request, *args, **kwargs):
        redis_cache.delete(self.get_cache_key())
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        redis_cache.delete(self.get_cache_key())
        return self.destroy(request, *args, **kwargs)
