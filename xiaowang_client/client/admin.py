from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'source','note', 'created_at']
    list_filter = ['source', 'owner__username']
    search_fields = ['source', 'phone', 'created_at']
    fields = ['name', 'phone', 'source', 'note']
