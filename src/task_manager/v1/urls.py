from django.urls import path
from task_manager.v1.views.task import TaskListAPIView, TaskDetailAPIView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("", TaskListAPIView.as_view()),
    path("<int:pk>/", TaskDetailAPIView.as_view()),
]
