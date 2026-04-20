from django.urls import path
from task_manager.v1.views import (
    TaskListAPIView,
    TaskDetailAPIView,
    tag_view,
    tag_detail_view,
)

urlpatterns = [
    path("", TaskListAPIView.as_view()),
    path("<int:pk>/", TaskDetailAPIView.as_view()),
    path("tags/", tag_view),
    path("tags/<int:pk>/", tag_detail_view),
]
