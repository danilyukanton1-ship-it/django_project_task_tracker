from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from task_manager.models import Tasks, Attachments, Comments
from account.models import User
from task_manager.forms import (
    CommentForm,
    TasksCreationForm,
    ChangeTask,
    AttachmentForm,
    DeleteTask,
)
from django.db import transaction
from django.core.paginator import Paginator
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.views import View
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse

tasks_list = [
    {"task_name": "Fix login bug", "status": "in progress", "priority": "high"},
    {"task_name": "Create navbar", "status": "done", "priority": "medium"},
    {"task_name": "Write tests", "status": "todo", "priority": "high"},
    {"task_name": "Update documentation", "status": "todo", "priority": "low"},
    {"task_name": "Deploy project", "status": "in progress", "priority": "medium"},
]

users = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 28},
    {"name": "Diana", "age": 22},
]


class TaskView(ListView):
    template_name = "tasks/tasks.html"
    model = Tasks

    paginate_by = 50
    paginator_class = Paginator
    context_object_name = "tasks"

    def get_queryset(self):
        return (
            Tasks.objects.select_related("assignee")
            .prefetch_related("tags", "comments")
            .all()
            .order_by("id")
        )


class Home(TemplateView):
    template_name = "tasks/home.html"


class About(TemplateView):
    template_name = "tasks/about.html"


class Index_2(View):
    def get(self, request, *args, **kwargs):
        task = kwargs["task"]
        return HttpResponse(f"<h1>Index 2. {task}</h1>")


class TaskListView(TemplateView):
    template_name = "tasks/tasks_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = tasks_list
        return context


class UserListView(TemplateView):
    template_name = "tasks/users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = users
        return context


class TasksWithComms(ListView):
    template_name = "tasks/comment_tasks.html"
    model = Tasks

    paginate_by = 50
    paginator_class = Paginator
    context_object_name = "tasks"

    def get_queryset(self):
        return (
            Tasks.objects.filter(comments__isnull=False)
            .prefetch_related(
                "comments",
                "tags",
            )
            .select_related("assignee")
        )


class UserTaskView(ListView):
    model = Tasks
    template_name = "tasks/user_task.html"
    context_object_name = "tasks"

    def get_queryset(self):
        user = self.request.GET.get("user")

        if user:
            return (
                Tasks.objects.filter(assignee__email=user)
                .select_related("assignee")
                .prefetch_related("tags")
            )

        return Tasks.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        return context


def add_comment_form(request):
    task_name = request.session.get("pending_task_name")
    task = Tasks.objects.get(name=task_name)
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = User.objects.get(username=form.cleaned_data["user"])
            comment.task = task
            comment.save()
            messages.success(request, "Комментарий добавлен")
            return redirect(".")
    else:
        form = CommentForm()

    return render(request, "tasks/add_comment.html", {"form": form})


def add_task_form(request):
    if request.method == "POST":
        form = TasksCreationForm(request.POST)
        if form.is_valid():
            task = form.save()
            request.session["pending_task_name"] = task.name
            messages.success(request, message="Задача добавлена")
            return redirect("add_comments")
    else:
        form = TasksCreationForm()

    return render(request, "tasks/add_task.html", {"form": form})


class AddTaskView(CreateView):
    model = Tasks
    form_class = TasksCreationForm
    template_name = "tasks/add_task.html"
    success_url = reverse_lazy("add_comments")

    def form_valid(self, form):
        task = form.save()
        self.request.session["pending_task_name"] = task.name
        messages.success(self.request, "Задача добавлена")
        return super().form_valid(form)


class AddCommentView(CreateView):
    model = Comments
    form_class = CommentForm
    template_name = "tasks/add_comment.html"
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        task_name = self.request.session.get("pending_task_name")
        task = Tasks.objects.get(name=task_name)
        comment = form.save(commit=False)
        print(type(comment))
        comment.task = task
        comment.name = User.objects.get(username=form.cleaned_data["user"])
        comment.save()

        messages.success(self.request, "Коммент создан удачно")
        return super().form_valid(form)


class DeleteTaskView(DeleteView):
    model = Tasks
    success_url = reverse_lazy("tasks")
    template_name = "tasks/tasks_confirm_delete.html"
    # template_name = "tasks_confirm_delete.html"
    # form_class = DeleteTask
    # pk_url_kwarg = "pk"


class AddTaskCommentView(CreateView):
    model = Tasks
    template_name = "tasks/add_task_comm.html"
    success_url = reverse_lazy("tasks")
    form_class = TasksCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form_2" not in kwargs:
            context["form2"] = "form_2"
        else:
            context["form2"] = kwargs["form2"]

    def post(self, request, *args, **kwargs):
        self.object = None

        task_form = TasksCreationForm(self.request.POST)
        com_form = CommentForm(self.request.POST)

        if task_form.is_valid() and com_form.is_valid():
            return self.form_valid(task_form, com_form)
        else:
            return self.form_invalid(task_form, com_form)

    @transaction.atomic
    def form_valid(self, task_form, com_form):
        task = task_form.save()

        self.request.session["pending_task_name"] = task.name
        comment = com_form.save(commit=False)
        comment.user = User.objects.get(username=com_form.cleaned_data["user"])
        comment.task = task
        comment.save()

        messages.success(self.request, "Задача создана")
        messages.success(self.request, "Коммент создан")

        return super().form_valid(task_form)

    def form_invalid(self, task_form, com_form):
        messages.error(self.request, "ERORR!!!")
        context = self.get_context_data(form=task_form, form2=com_form)
        return self.render_to_response(context)


# class AddTaskCommentView(CreateView):
#     model = Tasks
#     form_class = TasksCreationForm
#     template_name = 'add_task_com.html'
#     success_url = reverse_lazy('tasks')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if 'form2' not in kwargs:
#             context['form2'] = CommentForm()
#         else:
#             context['form2'] = kwargs['form2']
#         return context
#
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         task_form = self.get_form()
#         comment_form = CommentForm(request.POST)
#
#         if task_form.is_valid() and comment_form.is_valid():
#             return self.form_valid(task_form, comment_form)
#         else:
#             return self.form_invalid(task_form, comment_form)
#
#     @transaction.atomic
#     def form_valid(self, task_form, comment_form):
#         task = task_form.save()
#
#         self.request.session['pending_task_name'] = task.name
#
#         comment = comment_form.save(commit=False)
#         comment.user = User.objects.get(username=comment_form.cleaned_data['user'])
#
#         comment.task = task
#         comment.save()
#
#         messages.success(self.request, 'Задача добавлена')
#         messages.success(self.request, 'Комментарий добавлен')
#
#         return super().form_valid(task_form)
#
#     def form_invalid(self, task_form, comment_form):
#         messages.error(self.request, 'ERROR!!!!')
#         context = self.get_context_data(form1=task_form, form2=comment_form)
#         return self.render_to_response(context)


class EditTaskView(UpdateView):
    model = Tasks
    form_class = ChangeTask
    template_name = "tasks/change_task.html"
    success_url = reverse_lazy("tasks")
    pk_url_kwarg = "task_id"
    context_object_name = "task"


class CreateAttachmentView(CreateView):
    model = Attachments
    form_class = AttachmentForm
    template_name = "tasks/attachment_form.html"


class AttachmentsView(ListView):
    model = Attachments
    context_object_name = "attachments"
    template_name = "tasks/attachments.html"

    paginate_by = 50
    paginator_class = Paginator

    def get_queryset(self):
        return Attachments.objects.all().select_related("task")
