from account.models import User
from account.v1.serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["User"])
class UserAPIViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
