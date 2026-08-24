from django import forms
from .models import Post, Quiz

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'attachment']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['grade', 'group_number', 'questions']
