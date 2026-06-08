from account.v1.views import UserAPIViewSet
from rest_framework.routers import DefaultRouter

rest_router = DefaultRouter()
rest_router.register("", UserAPIViewSet, basename="user")

urlpatterns = []

urlpatterns += rest_router.urls
