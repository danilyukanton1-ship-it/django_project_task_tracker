import django_filters
from task_manager.models import Tasks


class TaskQueryFilterSerializer(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    priority_gt = django_filters.NumberFilter(field_name="priority", lookup_expr="gt")
    priority_lt = django_filters.NumberFilter(field_name="priority", lookup_expr="lt")

    class Meta:
        model = Tasks
        fields = ["name", "status", "priority"]


class TaskRequestUserFilterSerializer(django_filters.FilterSet):
    my_tasks = django_filters.BooleanFilter(method="filter_user_tasks")

    def filter_user_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(user=self.request.user)
        return queryset

    class Meta:
        model = Tasks
        fields = ["my_tasks"]
