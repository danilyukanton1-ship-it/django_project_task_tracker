from django.urls import path
from task_manager.v1.views import (
    TaskListAPIView,
    TaskDetailAPIView,
    tag_view,
    tag_detail_view,
    ProjectDetailsAPIView,
    ProjectDetailsDetailAPIView,
    ProjectAPIView,
    ProjectDetailAPIView,
)

urlpatterns = [
    path("", TaskListAPIView.as_view()),
    path("<int:pk>/", TaskDetailAPIView.as_view()),
    path("tags/", tag_view),
    path("tags/<int:pk>/", tag_detail_view),
    path("project-details/", ProjectDetailsAPIView.as_view()),
    path("project-details/<int:pk>/", ProjectDetailsDetailAPIView.as_view()),
    path("projects/", ProjectAPIView.as_view()),
    path("projects/<int:pk>/", ProjectDetailAPIView.as_view()),
]
