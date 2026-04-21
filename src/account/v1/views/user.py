from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import User
from account.v1.serializers import UserSerializer
from rest_framework import status
from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema


@extend_schema("User")
class UserAPIViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
