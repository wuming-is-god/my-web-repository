from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [('publish', '发布'), ('draft', '草稿')]

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
        related_name='article')
    name = models.CharField(max_length=20, null=False)
    title = models.CharField(max_length=30, null=False)
    content = models.TextField(null=True)
    status = models.CharField(max_length=10, default='publish', choices=STATUS_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'tb_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
        related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, 
        related_name='comments')
    content = models.TextField(blank=False)
    status =  models.CharField(max_length=10, default='publish', choices=STATUS_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'tb_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name