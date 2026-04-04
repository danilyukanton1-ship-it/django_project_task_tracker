from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from .models import Tasks
from account.models import User
from .forms import TaskForm
from django.db import transaction

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


def create_task(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TaskForm(request.POST)
        # check whether it's valid:

        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            form.save()
            return HttpResponseRedirect("/tasks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TaskForm()

    return render(request, "task_form.html", {"form": form})


def comment_tasks(request):
    task = Tasks.objects.filter(comments__isnull=False).prefetch_related('comments', 'tags',).select_related('assignee')
    context = {
        'tasks': task
    }
    return render(request, 'comment_tasks.html', context)


def user_task(request):
    users = User.objects.all()

    user = request.GET.get('user')

    if user:
        task = Tasks.objects.filter(assignee__email=user)

    else:
        task = Tasks.objects.none()

    context = {
        'tasks': task,
        'users': users
    }
    return render(request, 'user_task.html', context)
