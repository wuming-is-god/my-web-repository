from django import forms
from .models import Article, Comment
from django.forms import Textarea
from django.core.exceptions import ValidationError

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content','name']
        
    def clean_title(self):
        """验证标题"""
        title = self.cleaned_data.get('title')
        if len(title) <=5:
            raise ValidationError("标题字数不够")
        return title

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
       
    def clean_comment(self):
        content = self.cleaned_data.get('content')
        if len(comment) >= 100:
            raise ValidationError("评论字数过多")
        return content