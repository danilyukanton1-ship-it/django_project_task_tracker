from rest_framework import serializers
from django_celery_beat.models import PeriodicTask

class PeriodicTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = '__all__'