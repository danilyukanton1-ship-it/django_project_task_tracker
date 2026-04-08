from django import forms
from task_manager.models import Attachments


class AttachmentForm(forms.ModelForm):
    photo = forms.MultiValueField()

    class Meta:
        fields = [
            'name',
            'task',
            'photo'
        ]
        labels = {
            'name': 'Наименование',
            'task': 'Задача',
            'photo': 'Фотография'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите наименование для вложения'
            }),
            'task': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите задачу к которой хотите добавить вложение'
            })

        }
