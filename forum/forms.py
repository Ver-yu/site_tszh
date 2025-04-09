from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment

User = get_user_model()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Введите комментарий...'}),
        }