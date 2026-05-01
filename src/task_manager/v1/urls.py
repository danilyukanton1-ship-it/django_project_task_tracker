from django.urls import path
from rest_framework.routers import DefaultRouter
from task_manager.v1.views import (
    TaskAPIViewSet,
    tag_view,
    tag_detail_view,
    tag_tasks_view,
    ProjectDetailsAPIView,
    ProjectDetailsDetailAPIView,
    ProjectAPIView,
    ProjectDetailAPIView,
    CommentAPIView,
    CommentDetailAPIView,
    AttachmentAPIView,
    AttachmentDetailAPIView,
)

router = DefaultRouter()
router.register("", TaskAPIViewSet, basename="task")

urlpatterns = [
    path("tags/", tag_view),
    path("tags/<int:pk>/", tag_detail_view),
    path("tags/<int:pk>/tasks/", tag_tasks_view),
    path("project-details/", ProjectDetailsAPIView.as_view()),
    path("project-details/<int:pk>/", ProjectDetailsDetailAPIView.as_view()),
    path("projects/", ProjectAPIView.as_view()),
    path("projects/<int:pk>/", ProjectDetailAPIView.as_view()),
    path("comments/", CommentAPIView.as_view()),
    path("comments/<int:pk>/", CommentDetailAPIView.as_view()),
    path("attachments/", AttachmentAPIView.as_view()),
    path("attachments/<int:pk>/", AttachmentDetailAPIView.as_view()),
]

urlpatterns += router.urls
