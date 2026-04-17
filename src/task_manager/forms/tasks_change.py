from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from task_manager.models import Tasks, Tags
from django.core.exceptions import ValidationError


class ChangeTask(forms.ModelForm):
    priority = forms.IntegerField(
        label="Приоритет задачи",
        validators=[
            MinValueValidator(1, message="Приоритет не может быть меньше 1"),
            MaxValueValidator(5, message="Приоритет не может быть больше 5"),
        ],
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите приоритет для вашей задачи",
                "min": 1,
                "max": 5,
            }
        ),
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-control"}),
        required=False,
        label="Тэги",
    )

    class Meta:
        model = Tasks
        fields = ["name", "priority", "status", "description", "tags"]
        labels = {
            "name": "Имя задачи",
            "status": "Статус задачи",
            "description": "Описание задачи",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "special",
                    "placeholder": "Введите имя для вашей задачи",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Выберите статус для задачи",
                }
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "cols": 10}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        priority = cleaned_data.get("priority")
        description = cleaned_data.get("description").strip()
        if priority == 5 and not description:
            raise ValidationError(
                "Пока в задаче нет описания, вы не можете поставить максимальный приоритет"
            )
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["tags"].initial = self.instance.tags.all()
