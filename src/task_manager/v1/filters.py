import django_filters
from task_manager.models import Tasks


class TaskQueryFilterSerializer(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    priority_gt = django_filters.NumberFilter(field_name="priority", lookup_expr="gt")
    priority_lt = django_filters.NumberFilter(field_name="priority", lookup_expr="lt")

    class Meta:
        model = Tasks
        fields = ["name", "status", "priority"]
