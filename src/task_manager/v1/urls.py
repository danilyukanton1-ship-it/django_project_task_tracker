from django.urls import path
from task_manager.v1.views.task import TaskListAPIView, TaskDetailAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
urlpatterns = [
    path("tasks/", TaskListAPIView.as_view()),
    path("tasks/<int:pk>/", TaskDetailAPIView.as_view()),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]