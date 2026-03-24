from django.shortcuts import render

from django.http import HttpResponse
from .models import Tasks

tasks_list = [
    {"task_name": "Fix login bug", "status": "in progress", "priority": "high"},
    {"task_name": "Create navbar", "status": "done", "priority": "medium"},
    {"task_name": "Write tests", "status": "todo", "priority": "high"},
    {"task_name": "Update documentation", "status": "todo", "priority": "low"},
    {"task_name": "Deploy project", "status": "in progress", "priority": "medium"}
]

users = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 28},
    {"name": "Diana", "age": 22}
]


def tasks(request):
    """
    :param request:
    :return: page with tasks
    """
    context = {
        'tasks': Tasks.objects.select_related('assignee').prefetch_related('tags', 'comments').all()
    }
    return render(request, 'tasks.html', context)


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def index_2(request, task):
    return HttpResponse(f'<h1>Index 2. {task}</h1>')


def task_list_view(request):
    """

    :param request:
    :return: shows tasks from our list
    """
    context = {
        'tasks': tasks_list
    }
    return render(request, 'tasks_list.html', context)


def user_list(request):
    """
    :param request:
    :return: shows users from our another list
    """
    context = {
        'users': users
    }
    return render(request, 'users.html', context)