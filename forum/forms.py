from django import forms
from .models import Post, Poll, Comment
from users.mixins import TSZHMemberRequiredMixin

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class PollForm(forms.ModelForm):
    options = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Введите варианты ответов через запятую"
    )

    class Meta:
        model = Poll
        fields = ['question']

    def clean_options(self):
        options = self.cleaned_data['options'].split(',')
        return {option.strip(): 0 for option in options if option.strip()}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }