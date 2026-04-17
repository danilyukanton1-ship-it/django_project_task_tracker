from django import forms
from task_manager.models import Attachments
from PIL import Image


class AttachmentForm(forms.ModelForm):
    photo = forms.FileField(
        label="Фото",
        required=False,
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control-file", "accept": "image/*"}
        ),
    )

    # photo = forms.FileField(
    #     label='Файл',
    #     required=False,
    #     widget=forms.ClearableFileInput(attrs={
    #         'class':'form-control-file'
    #     })
    # )

    class Meta:
        model = Attachments
        fields = ["name", "task", "photo"]
        labels = {"name": "Наименование", "task": "Задача", "photo": "Фотография"}
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите наименование для вложения",
                }
            ),
            "task": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите задачу к которой хотите добавить вложение",
                }
            ),
        }

    def clean_photo(self):
        cleaned_photo = self.cleaned_data.get("photo")
        if cleaned_photo:
            # type checking
            try:
                img = Image.open(cleaned_photo)
                img.verify()
            except Exception:
                raise forms.ValidationError("Файл должен быть изображением")
            # size checking
            if cleaned_photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Размер файла слишком большой")
        return cleaned_photo
