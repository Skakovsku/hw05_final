from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {
            'text': 'Поле для ввода текста поста',
            'group': 'Выбирите подходящий вариант группы',
            'image': 'Загрузите изображение',
        }

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Вы забыли напечатать текст поста')
        return data


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = {'text'}
        help_texts = {
            'text': 'Напишите свой комментарий к посту'
        }
