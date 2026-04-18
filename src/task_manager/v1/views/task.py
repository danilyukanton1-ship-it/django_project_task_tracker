from gc import get_objects

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from task_manager.models import Tasks
from task_manager.v1.serializers import TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from django.core.cache import caches
from django.shortcuts import get_object_or_404

redis_cache = caches["redis"]

# @csrf_exempt
# def tasks_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == "GET":
#         tasks = Tasks.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = TaskSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# def task_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         task = Tasks.objects.get(pk=pk)
#     except Tasks.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == "GET":
#         serializer = TaskSerializer(task)
#         return JsonResponse(serializer.data)
#
#     elif request.method == "PUT":
#         data = JSONParser().parse(request)
#         serializer = TaskSerializer(task, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == "DELETE":
#         task.delete()
#         return HttpResponse(status=204)

# @api_view(["GET", "POST"])
# def tasks_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == "GET":
#         snippets = Tasks.objects.all()
#         serializer = TaskSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == "POST":
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(["GET", "PUT", "DELETE"])
# def tasks_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Tasks.objects.get(pk=pk)
#     except Tasks.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = TaskSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == "PUT":
#         serializer = TaskSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == "DELETE":
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class TaskListAPIView(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#
#     def get(self, request, format=None):
#         tasks = Tasks.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class TaskDetailAPIView(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#
#     def get_object(self, pk):
#         try:
#             return Tasks.objects.get(pk=pk)
#         except Tasks.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         task = self.get_object(pk)
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Task"])
class TaskListAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

    @extend_schema(responses={201: TaskSerializer})
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(request=TaskSerializer, responses={201: TaskSerializer})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@extend_schema(tags=["Task"])
class TaskDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Tasks.objects.all()
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
