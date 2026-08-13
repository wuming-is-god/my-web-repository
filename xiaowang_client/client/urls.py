from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'client'

urlpatterns = [
    # 登录
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # 登出
    path('logout/', views.user_logout, name='logout'),
    # 注册
    path('register/', views.register , name='register'),
    # 客户信息填写
    path('client/create/',views.ClientCreateView.as_view()  , name='client_create'),
    # 客户信息列表
    path('client/list/',views.ClientListView.as_view() , name='client_list'),
    # 客户信息搜索
    path('client/search/',views.client_search , name='client_search'),
    # 客户信息删除
    path('client/delete/<int:pk>/',views.client_delete , name='client_delete'),
    # 客户信息详情
    path('client/update/<int:pk>/',views.ClientUpdateView.as_view() , name='client_update'),
]