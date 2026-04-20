__all__ = (
    "TaskListAPIView",
    "TaskDetailAPIView",
    "tag_view",
    "tag_detail_view",
    "ProjectDetailsView",
    "ProjectDetailsDetailView",
)

from task_manager.v1.views.task import TaskListAPIView
from task_manager.v1.views.task import TaskDetailAPIView
from task_manager.v1.views.tag import tag_detail_view
from task_manager.v1.views.tag import tag_view
from task_manager.v1.views.project_detail import ProjectDetailsView
from task_manager.v1.views.project_detail import ProjectDetailsDetailView
