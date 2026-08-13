from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User

def register(request):
    """注册"""
    if request.method != 'POST':
        # 创建表单
        form = UserCreationForm() 
    else:
        # 检验
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 登录
            login(request, user)
            return redirect(reverse('user:personal_page'))
    context = {
            'form': form
        }        
    return render(request, 'registration.html', context)


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def user_logout(request):
    '登出'
    logout(request)
    return redirect(reverse('user:login'))
    
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.shortcuts import get_object_or_404, reverse
from django.db.models import Sum, Count, Avg, Q, F
from django.urls import reverse_lazy
from django.http import JsonResponse

class PersonalPage(LoginRequiredMixin, DetailView):
    """个人主页"""
    model = Article
    template_name = 'personal_page.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        """获取个人信息"""
        # 获取上下文
        context = super().get_context_data(**kwargs)
        # 用户名
        username = self.request.user.username
        # 用户文章数和文章标题
        articles = Article.objects.filter(author=self.request.user)
        article_count = articles.count()
       
        titles_dict = {article.pk: article.title for article in articles }
        # 用户文章受到评论的总数 
        comment_count = articles.aggregate(comment_count=Count('comments'))['comment_count']
        # 添加上下文    
        context['username'] = username 
        context['article_count'] = article_count
        context['titles_dict'] = titles_dict
        context['comment_count'] = comment_count
        return context


class Public(LoginRequiredMixin, ListView):
    """公共界面"""
    template_name = 'public.html'
    context_object_name = 'articles'
    
    def get_queryset(self):
        """获取文章标题"""
        articles = Article.objects.filter(title__isnull=False)
        return articles

    def get_context_data(self, **kwargs):
        """添加上下文"""
        context = super().get_context_data(**kwargs)
        # 用户总数
        users_count = User.objects.count()
        # 文章总数
        articles_count = context['articles'].count()
        # 评论总数
        comments_count = Comment.objects.count()
        context['users_count'] = users_count
        context['articles_count'] = articles_count
        context['comments_count'] = comments_count
        return context

class CreateArticle(LoginRequiredMixin, CreateView):
    """创建文章"""
    form_class = ArticleForm
    template_name = 'create_article.html'

    def form_valid(self, form):
        """添加用户"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """跳转到该文章显示页面"""
        return reverse('user:article_display', kwargs={'pk': self.object.pk})

class ArticleDisplay(LoginRequiredMixin, DetailView):
    """显示用户查看的文章"""
    template_name = 'article_display.html'
    context_object_name = 'article'

    def get_object(self):
        """获取该文章"""
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        return article
    

class EditArticle(LoginRequiredMixin, UpdateView):
    """编辑已有文章"""
    form_class = ArticleForm
    template_name = 'edit_article.html'
    context_object_name = 'article'

    def get_object(self):
        """获取该文章"""
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'), 
            author=self.request.user)
        return article
    def get_success_url(self):
        """编辑完成后,跳转页面"""
        return reverse('user:article_display', kwargs={'pk': self.kwargs.get('pk')})

class DeleteArticle(LoginRequiredMixin, DeleteView):
    """删除文章"""
    context_object_name = 'article'
    success_url = reverse_lazy('user:personal_page')
    template_name = 'delete_article.html'

    def get_object(self):
        """获取该文章"""
        article = get_object_or_404(Article, pk=self.kwargs.get("pk"), 
            author=self.request.user)
        return article
    def delete(self, request, *args, **kwargs):
        """删除文章"""
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.object.delete()
            return JsonResponse({'status': 'ok', 'message': '删除成功'})
        else:
            return super().delete(request, *args, **kwargs)
   
    
class CreateComment(LoginRequiredMixin, CreateView):
    """创建评论"""
    form_class = CommentForm
    template_name = 'create_comment.html'
    context_object_name = 'comment'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article = Article.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    def get_success_url(self):
        """跳转到文章显示页面"""
        return reverse('user:article_display', kwargs={'pk': self.kwargs.get('pk')})

def practice(request):
    return render(request, 'practice.html')

def search(request):
    query = request.GET.get('q', '')
    if query:
        article = Article.objects.filter(title__icontains=query)
        suggestions = [{'id': a.id, 'title': a.title} for a in article]
    else:
        suggestions = []
    return JsonResponse({'suggestions': suggestions})