from django.urls import path, re_path, include
from task_manager.views import (
    TaskView,
    Index_2,
    About,
    TaskListView,
    UserListView,
    Home,
    UserTaskView,
    TasksWithComms,
    AddCommentView,
    AddTaskView,
    EditTaskView,
    AddTaskCommentView,
    CreateAttachmentView,
    AttachmentsView,
    DeleteTaskView,
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("about/", About.as_view(), name="about"),
    path("tasks/", TaskView.as_view(), name="tasks"),
    path("tasks-list/", TaskListView.as_view(), name="task_list"),
    path("users/", UserListView.as_view(), name="users"),
    re_path(r"^details/(?P<task>[0-9]{4})/$", Index_2.as_view()),
    path("tasks/user_task/", UserTaskView.as_view(), name="user_task"),
    path("tasks/comment_tasks/", TasksWithComms.as_view(), name="comment_tasks"),
    path("tasks/add_comment/", AddCommentView.as_view(), name="add_comments"),
    path("tasks/add_tasks/", AddTaskView.as_view(), name="add_tasks"),
    path("tasks/<int:task_id>/edit/", EditTaskView.as_view(), name="change_task"),
    path("tasks/add_task_com/", AddTaskCommentView.as_view(), name="add_task_comment"),
    path(
        "tasks/create_attach/", CreateAttachmentView.as_view(), name="create_attachment"
    ),
    path("tasks/attachments/", AttachmentsView.as_view(), name="attachments"),
    path("tasks/<int:pk>/delete/", DeleteTaskView.as_view(), name="delete_task"),
]
