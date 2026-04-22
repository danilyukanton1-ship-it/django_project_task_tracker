from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from task_manager.v1.serializers import TagSerializer
from rest_framework.decorators import api_view
from task_manager.models import Tags
from rest_framework.parsers import JSONParser
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from task_manager.v1.serializers import TaskSerializer
from rest_framework.response import Response


@extend_schema(tags=["Tag"])
@api_view(["GET", "POST"])
def tag_view(request):
    if request.method == "GET":
        tags = Tags.objects.annotate(tasks_count=Count("tasks"))
        pagination = PageNumberPagination()
        pagination.page_size = 20
        page = pagination.paginate_queryset(tags, request)
        serializer = TagSerializer(page, many=True)
        return pagination.get_paginated_response(serializer.data)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = TagSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@extend_schema(tags=["Tag"])
@api_view(["GET", "PUT", "DELETE"])
def tag_detail_view(request, pk):
    try:
        tag = Tags.objects.get(pk=pk)
    except Tags.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = TagSerializer(tag, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        tag.delete()
        return HttpResponse(status=204)


@extend_schema(tags=["Tag"])
@api_view(["GET"])
def tag_tasks_view(request, pk):
    try:
        tag = Tags.objects.get(pk=pk)
    except Tags.DoesNotExist:
        return HttpResponse(status=404)

    tasks = tag.tasks.select_related("assignee", "project").all()

    pagination = PageNumberPagination()
    pagination.page_size = 50

    page = pagination.paginate_queryset(tasks, request)
    serializer = TaskSerializer(page, many=True)
    return pagination.get_paginated_response(serializer.data)
