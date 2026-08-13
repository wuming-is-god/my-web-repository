from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'user'
urlpatterns = [
    # 注册
   path('register/', views.register, name='register'),
   # 登录
   path('login/', LoginView.as_view(template_name='login.html'), name='login'),
   # 登出
   path('logout/', views.user_logout, name='logout'),
   # 个人主页
   path('personal/page/', views.PersonalPage.as_view(), name='personal_page'),
   # 公共界面
   path('', views.Public.as_view(), name='public'),
   # 创建文章
   path('create/article/', views.CreateArticle.as_view(), name='create_article'),
   # 文章显示 
   path('article/display/<int:pk>', views.ArticleDisplay.as_view(), name='article_display'),
   # 文章编辑
   path('edit/article/<int:pk>/', views.EditArticle.as_view(), name='edit_article'),
   # 删除文章
   path('delete/article/<int:pk>/', views.DeleteArticle.as_view(), name='delete_article'),
   # 创建评论
   path('create/comment/<int:pk>/', views.CreateComment.as_view(), name='create_comment'),
   # 练习
   path('practice/', views.practice)
]