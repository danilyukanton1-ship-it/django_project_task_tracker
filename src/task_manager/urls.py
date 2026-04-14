from django.urls import path, re_path, include
from .views import (
    TaskView,
    Index_2,
    About,
    task_list_view,
    user_list,
    home,
    create_task,
    user_task,
    comment_tasks,
    add_comment_form,
    add_task_form,
    change_task_form,
    add_task_comment,
    create_attachment,
    attachments
    )


urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('about/', About.as_view(), name='about'),
    path('tasks/', TaskView.as_view(), name='tasks'),
    path('tasks-list/', task_list_view, name='task_list'),
    path('users/', user_list, name='users'),
    re_path(r"^details/(?P<task>[0-9]{4})/$", Index_2.as_view()),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/user_task/', user_task, name='user_task'),
    path('tasks/comment_tasks/', comment_tasks, name='comment_tasks'),
    path('tasks/add_comment/', add_comment_form, name='add_comments'),
    path('tasks/add_tasks/', add_task_form, name='add_tasks'),
    path('tasks/change_tasks/<int:task_id>/', change_task_form, name='change_task'),
    path('tasks/add_task_com/', add_task_comment, name='add_task_comment'),
    path('tasks/create_attach/', create_attachment, name='create_attachment'),
    path('tasks/attachments/', attachments, name='attachments'),
    path('tasks/api/', include('task_manager.v1.urls')),
]

