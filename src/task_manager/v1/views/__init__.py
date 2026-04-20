__all__ = (
    "TaskListAPIView",
    "TaskDetailAPIView",
    "tag_view",
    "tag_detail_view",
    "ProjectDetailsAPIView",
    "ProjectDetailsDetailAPIView",
    "ProjectAPIView",
    "ProjectDetailAPIView",
    "CommentAPIView",
    "CommentDetailAPIView",
)

from task_manager.v1.views.task import TaskListAPIView
from task_manager.v1.views.task import TaskDetailAPIView
from task_manager.v1.views.tag import tag_detail_view
from task_manager.v1.views.tag import tag_view
from task_manager.v1.views.project_detail import ProjectDetailsAPIView
from task_manager.v1.views.project_detail import ProjectDetailsDetailAPIView
from task_manager.v1.views.project import ProjectAPIView
from task_manager.v1.views.project import ProjectDetailAPIView
from task_manager.v1.views.comment import CommentAPIView
from task_manager.v1.views.comment import CommentDetailAPIView
