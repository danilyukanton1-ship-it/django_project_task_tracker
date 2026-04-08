from django import forms
from task_manager.models import Comments, Tasks
from account.models import User


class CommentForm(forms.ModelForm):
    task = forms.CharField(
        max_length=64,
        label='Задача',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ID или название задачи'
        })
    )
    user = forms.CharField(
        max_length=64,
        label='Автор комментария',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите никнейм пользователя'
        })

    )

    class Meta:
        model = Comments
        fields = ['task', 'user', 'message']

        labels = {
            'message': 'Комментарий'
        }

        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ввелдите текст комментария'
            }),
        }

    def clean_task(self):
        task_input = self.cleaned_data.get('task')

        if str(task_input).isdigit():
            try:
                task = Tasks.objects.get(id=int(task_input))
                return task
            except Tasks.DoesNotExist:
                pass

        try:
            task = Tasks.objects.get(name=task_input)
            return task
        except Tasks.DoesNotExist:
            er = forms.ValidationError('Задача не найдена')
            raise er

    def clean_user(self):
        username = self.cleaned_data['user']

        if str(username).isdigit():
            try:
                return User.objects.get(id=int(username))
            except User.DoesNotExist:
                pass

        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Пользователь не найден')
