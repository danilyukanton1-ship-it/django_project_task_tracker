from django.http import HttpResponse, JsonResponse

from task_manager.v1.serializers import TagSerializer
from rest_framework.decorators import api_view
from task_manager.models import Tags
from rest_framework.parsers import JSONParser
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Tag"])
@api_view(["GET", "POST"])
def tag_view(request):
    if request.method == "GET":
        tags = Tags.objects.all().prefetch_related("tasks")
        serializer = TagSerializer(tags, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = TagSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@extend_schema(tags=["Tag"])
@api_view(["GET", "PUT", "DELETE"])
def tag_detail_view(request, pk):
    try:
        tag = Tags.objects.get(pk=pk)
    except Tags.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = TagSerializer(tag)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = TagSerializer(tag, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        tag.delete()
        return HttpResponse(status=204)
