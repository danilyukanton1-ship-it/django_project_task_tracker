from django.urls import path, re_path
from .views import tasks, index_2, about, task_list_view, user_list, home


urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('about/', about, name='about'),
    path('tasks/', tasks, name='tasks'),
    path('tasks-list/', task_list_view, name='task_list'),
    path('users/', user_list, name='users'),
    re_path(r"^details/(?P<task>[0-9]{4})/$", index_2),
]
