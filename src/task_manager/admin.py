from django.contrib import admin
from task_manager.models import (
    Tasks,
    Tags,
    Projects,
    ProjectDetails,
    Comments,
    Attachments,
)
from django.contrib.admin import SimpleListFilter
from django.utils.html import format_html


# admin actions
@admin.action(description="Make completed")
def make_completed(model_admin, request, queryset):
    queryset.update(status="Completed")


@admin.action(description="Make canceled")
def make_canceled(model_admin, request, queryset):
    queryset.update(status="Canceled")


@admin.action(description="Make not reopened")
def make_not_reopened(model_admin, request, queryset):
    queryset.update(is_reopened=False)


@admin.action(description='Add comment "Processed by admin"')
def make_admin_comment(model_admin, request, queryset):
    comments_created = 0
    for task in queryset:
        comment = Comments.objects.create(
            task=task,
            message=f"Processed by admin ",
            user=request.user,
        )
        comments_created += 1
    model_admin.message_user(
        request,
        f"Added {comments_created} comments to chosen tasks",
    )


# filter


class AssigneeFilter(SimpleListFilter):
    parameter_name = "assignee"
    title = "assignee filter"

    def lookups(self, request, model_admin):
        return [("null", "Without assignee"), ("not_null", "With assignee")]

    def queryset(self, request, queryset):

        if self.value() == "null":
            return queryset.filter(assignee__isnull=True)

        if self.value() == "not_null":
            return queryset.filter(assignee__isnull=False)

        return queryset


# inline


class CommentInline(admin.TabularInline):
    model = Comments
    extra = 1


class TagInline(admin.TabularInline):
    model = Tags.tasks.through
    extra = 1


class AttachmentInline(admin.StackedInline):
    model = Attachments
    extra = 1


@admin.register(Tasks)
class TaskAdmin(admin.ModelAdmin):
    def priority_status(self, obj):
        if obj.priority < 3:
            return "Low"
        elif obj.priority < 5:
            return "Medium"
        else:
            return "High"

    priority_status.string = ""
    priority_status.short_description = "Приоритет статуса"

    fieldsets = (
        (
            None,
            {
                "fields": (("name", "status"), "description"),
            },
        ),
        (
            "Additional",
            {
                "fields": (
                    "priority",
                    "project",
                    "assignee",
                    "created_at",
                    "num_of_coms",
                    "is_reopened",
                ),
            },
        ),
    )

    list_display = [
        "name",
        "status",
        "priority",
        "assignee",
        "priority_status",
        "with_email",
    ]
    list_display_links = ["name", "priority_status"]
    list_editable = ["priority", "status"]
    list_filter = [
        AssigneeFilter,
        "status",
        "priority",
        "project",
    ]
    search_fields = ["name", "assignee__email"]
    list_per_page = 20
    ordering = ["priority", "name"]
    readonly_fields = ["created_at", "num_of_coms"]
    inlines = [CommentInline, TagInline, AttachmentInline]
    actions = [
        make_completed,
        make_canceled,
        make_not_reopened,
        make_admin_comment,
    ]

    @admin.display(description="email of the assignee", ordering="assignee__email")
    def with_email(self, obj):
        return obj.assignee.email

    @admin.display(description="Number of comments")
    def num_of_coms(self, obj):
        return obj.comments.count()


# Стакд тут удобнее так как места хвататет и писать информацию о проекте так удобнее
class ProjectDetailsInline(admin.StackedInline):
    model = ProjectDetails
    extra = 1


@admin.register(Projects)
class AdminProject(admin.ModelAdmin):
    fields = ["name", "description"]
    # exclude = ['owner']
    inlines = [ProjectDetailsInline]


@admin.register(Attachments)
class AttachmentsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "task", "photo"]
    raw_id_fields = ["task"]

    @admin.display(description="photo showing")
    def display_photo(self, instance):
        if instance.photo:
            return format_html('<img src="{}" width=50/>', instance.photo.url)


admin.site.register(Tags)
admin.site.register(ProjectDetails)
admin.site.register(Comments)
