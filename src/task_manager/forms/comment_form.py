from django import forms
from task_manager.models import Comments, Tasks
from account.models import User


class CommentForm(forms.ModelForm):
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
        fields = ['user', 'message']

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
