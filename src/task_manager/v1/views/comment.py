from rest_framework.views import APIView
from rest_framework.response import Response

from config.pagination import CustomPagination
from task_manager.v1.serializers import CommentSerializer
from task_manager.models import Comments
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.http import Http404
from rest_framework import status


@extend_schema(tags=["Comment"])
class CommentAPIView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="page", description="Page number", required=False, type=int
            ),
        ]
    )
    def get(self, request):
        comments = Comments.objects.select_related("user", "task").all()

        paginator = CustomPagination()
        page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Comment"])
class CommentDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Comments.objects.get(pk=pk)
        except Comments.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
