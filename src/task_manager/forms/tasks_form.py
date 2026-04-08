from django import forms
from task_manager.models import Tasks
from django.core.validators import MinValueValidator, MaxValueValidator


class TasksCreationForm(forms.ModelForm):
    priority = forms.IntegerField(
        label='Приоритет задачи',
        validators=[
            MinValueValidator(1, message='Приоритет не может быть меньше 1'),
            MaxValueValidator(5, message='Приоритет не может быть больше 5')
        ],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите приоритет для вашей задачи',
            'min': 1,
            'max': 5,

        })
    )

    class Meta:
        model = Tasks
        fields = ['name', 'priority', 'description', 'status']
        labels = {
            'name': 'Имя задачи',
            'status': 'Статус задачи',
            'description': 'Описание задачи'
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'special',
                'rows': 3,
                'placeholder': 'Введите описание задачи'
            }),
            'name': forms.TextInput(attrs={
                'class': 'special',
                'placeholder': 'Введите имя для вашей задачи'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите статус для задачи'
            })
        }

