from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin  # 可选，用于继承
from django.utils.translation import ngettext
from .models import Article, Comment

# ========== 先注销默认的 User 注册 ==========
admin.site.unregister(User)

# ========== 文章内联（在用户编辑页展示其所有文章） ==========
class ArticleInline(admin.TabularInline):
    model = Article
    fk_name = 'author'
    extra = 1
    fields = ('title', 'status', 'created_date')
    readonly_fields = ('created_date',)

# ========== 评论内联（在文章编辑页展示其所有评论） ==========
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('user', 'content', 'status', 'created_date')
    readonly_fields = ('created_date',)

# ========== 用户（User）后台 ==========
@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'date_joined']
    list_filter = ['is_active', 'date_joined']
    search_fields = ['username', 'email']
    ordering = ['-date_joined']
    fields = ['username', 'email', 'password', 'is_active', 'date_joined']
    readonly_fields = ['date_joined']   # 注册时间不可修改
    inlines = [ArticleInline]
    actions = ['make_active']

    @admin.action(description='将选中的账号设为激活状态')
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)   # 布尔值，非字符串
        self.message_user(
            request,
            ngettext(
                "%d 个账号已成功激活。",
                "%d 个账号已成功激活。",
                updated
            ) % updated,
            messages.SUCCESS
        )

# ========== 文章（Article）后台 ==========
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_date', 'comment_count']
    list_filter = ['status', 'author', 'created_date']
    search_fields = ['title', 'content', 'author__username']
    ordering = ['-created_date']
    fieldsets = (
        (None, {
            'fields': ('author', 'name', 'title', 'content', 'status')
        }),
        ('时间信息', {
            'classes': ('collapse',),
            'fields': ('created_date', 'update_date')
        }),
    )
    readonly_fields = ('created_date', 'update_date')
    inlines = [CommentInline]

    @admin.display(description='评论数', ordering='comment_count')
    def comment_count(self, obj):
        return obj.comments.count()

# ========== 评论（Comment）后台 ==========
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'content_preview', 'status', 'created_date']
    list_filter = ['status', 'created_date']
    search_fields = ['user__username', 'article__title', 'content']
    ordering = ['-created_date']
    fields = ['user', 'article', 'content', 'status', 'created_date']
    readonly_fields = ['created_date']

    @admin.display(description='内容预览')
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content