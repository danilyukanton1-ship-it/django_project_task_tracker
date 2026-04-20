from django.urls import path
from task_manager.v1.views.task import TaskListAPIView, TaskDetailAPIView

urlpatterns = [
    path("", TaskListAPIView.as_view()),
    path("<int:pk>/", TaskDetailAPIView.as_view()),
]
