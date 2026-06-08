__all__ = (
    "TaskAPIViewSet",
    "tag_view",
    "tag_detail_view",
    "tag_tasks_view",
    "ProjectDetailsAPIView",
    "ProjectDetailsDetailAPIView",
    "ProjectAPIView",
    "ProjectDetailAPIView",
    "CommentAPIView",
    "CommentDetailAPIView",
    "AttachmentAPIView",
    "AttachmentDetailAPIView",
    "PeriodicTaskViewSet",
)

from task_manager.v1.views.task import TaskAPIViewSet
from task_manager.v1.views.tag import tag_detail_view
from task_manager.v1.views.tag import tag_view
from task_manager.v1.views.tag import tag_tasks_view
from task_manager.v1.views.project_detail import ProjectDetailsAPIView
from task_manager.v1.views.project_detail import ProjectDetailsDetailAPIView
from task_manager.v1.views.project import ProjectAPIView
from task_manager.v1.views.project import ProjectDetailAPIView
from task_manager.v1.views.comment import CommentAPIView
from task_manager.v1.views.comment import CommentDetailAPIView
from task_manager.v1.views.attachment import AttachmentAPIView
from task_manager.v1.views.attachment import AttachmentDetailAPIView
from task_manager.v1.views.periodic_task import PeriodicTaskViewSet
