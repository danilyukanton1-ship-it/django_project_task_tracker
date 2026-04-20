from django.urls import path
from task_manager.v1.views import (
    TaskListAPIView,
    TaskDetailAPIView,
    tag_view,
    tag_detail_view,
    ProjectDetailsView,
    ProjectDetailsDetailView,
)

urlpatterns = [
    path("", TaskListAPIView.as_view()),
    path("<int:pk>/", TaskDetailAPIView.as_view()),
    path("tags/", tag_view),
    path("tags/<int:pk>/", tag_detail_view),
    path("project-details/", ProjectDetailsView.as_view()),
    path("project-details/<int:pk>/", ProjectDetailsDetailView.as_view()),
]
