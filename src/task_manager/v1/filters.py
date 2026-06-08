import django_filters
from task_manager.models import Tasks
from task_manager.models.tasks import TaskStatus


class TaskQueryFilterSerializer(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    priority = django_filters.NumberFilter(field_name="priority")
    priority_gt = django_filters.NumberFilter(field_name="priority", lookup_expr="gt")
    priority_lt = django_filters.NumberFilter(field_name="priority", lookup_expr="lt")
    status = django_filters.ChoiceFilter(
        field_name="status", choices=TaskStatus.choices
    )
    description = django_filters.CharFilter(
        field_name="description", lookup_expr="icontains"
    )
    created_at = django_filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Tasks
        fields = [
            "name",
            "status",
            "priority",
            "priority_gt",
            "priority_lt",
            "created_at",
            "description",
        ]
