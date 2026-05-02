from task_manager.models import Tasks, Comments
from task_manager.v1.serializers import TaskSerializer
from task_manager.v1.filters import TaskQueryFilterSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.core.cache import caches
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from config.pagination import CustomPagination
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend

redis_cache = caches["redis"]


@extend_schema(tags=["Task"])
class TaskAPIViewSet(ModelViewSet):
    queryset = Tasks.objects.select_related(
        "assignee", "project", "project__owner"
    ).prefetch_related(
        "tags", Prefetch("comments", queryset=Comments.objects.select_related("user"))
    )
    serializer_class = TaskSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = (TaskQueryFilterSerializer,)
    filterset_fields = {
        "created_at": ["lte", "gte"],
    }

    def get_queryset(self):
        user = self.request.user
        return (
            Tasks.objects.select_related("assignee", "project", "project__owner")
            .prefetch_related(
                "tags",
                Prefetch("comments", queryset=Comments.objects.select_related("user")),
            )
            .filter(assignee=user)
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
