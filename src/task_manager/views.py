from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Tasks, Comments
from account.models import User
from .forms import TaskForm, CommentForm, TasksCreationForm, ChangeTask
from django.db import transaction
from django.core.paginator import Paginator

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
    task = Tasks.objects.select_related('assignee').prefetch_related('tags', 'comments').all().order_by('id')
    paginator = Paginator(task, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'tasks': page_obj, 'page_obj': page_obj
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
    task = Tasks.objects.filter(comments__isnull=False).prefetch_related('comments', 'tags', ).select_related(
        'assignee')
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


def add_comment_form(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = User.objects.get(username=form.cleaned_data['user'])
            comment.task = Tasks.objects.get(name=form.cleaned_data['task'])
            comment.save()
            messages.success(request, 'Комментарий добавлен')
            return redirect('.')
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form})


def add_task_form(request):
    if request.method == "POST":
        form = TasksCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, message='Задача добавлена')
            return redirect('.')
    else:
        form = TasksCreationForm()

    return render(request, 'add_task.html', {'form': form})


def change_task_form(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
    if request.method == "POST":
        form = ChangeTask(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            # не получилось с save_m2m так и проблему найти не получилось
            tags_ids = [int(id) for id in request.POST.getlist('tags') if id]
            task.tags.set(tags_ids)
            messages.success(request, f'Задача "{task.name}" обновлена')
            return redirect('change_task', task_id=task.id)
    else:
        form = ChangeTask(instance=task)
    context = {'form': form,
               'task': task,
               }

    return render(request, 'change_task.html', context)
