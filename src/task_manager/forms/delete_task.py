from django import forms
from task_manager.models import Tasks


class DeleteTask(forms.ModelForm):

    class Meta:
        model = Tasks
        fields = ["name", "priority", "status", "description"]
        labels = {
            "name": "Имя задачи",
            "priority": "Приоритет задачи",
            "status": "Статус задачи",
            "description": "Описание задачи",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "priority": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
        }
