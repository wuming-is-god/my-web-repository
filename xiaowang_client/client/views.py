from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.db.models import Sum, Count, Avg, Q, F
from .models import Client
from .forms import ClientForm
from django.views.decorators.http import require_http_methods

def register(request):
    """注册"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect(reverse('client:client_create'))
    form = UserCreationForm()
    context = {'form':form}
    return render(request, 'register.html', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('client:login'))

class ClientCreateView(LoginRequiredMixin, CreateView):
    """客户信息填写"""
    model = Client
    form_class = ClientForm
    template_name = 'client_create.html'
    success_url = reverse_lazy('client:client_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class ClientListView(LoginRequiredMixin, ListView):
    """客户信息列表"""
    model = Client
    template_name = 'client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        clients = Client.objects.filter(owner=self.request.user).order_by('-created_at')[:5]
        return clients

@login_required
def client_search(request):
    phone = request.GET.get('phone', '').strip()
    source = request.GET.get('source', '').strip()

    clients_qs = Client.objects.filter(owner=request.user)
    if phone:
        clients_qs = clients_qs.filter(phone__icontains=phone)
    if source:
        clients_qs = clients_qs.filter(source=source)

    clients = list(clients_qs.order_by('-created_at').values('id', 'name', 'phone', 'source'))[:5]
    return JsonResponse({'state': 'success', 'clients': clients})

@require_http_methods(["DELETE"])
@login_required
def client_delete(request, pk):
    if not pk:
        return JsonResponse({'state': 'fail', 'error': 'pk为空'})
    try:
        client = Client.objects.get(pk=pk, owner=request.user)
    except Client.DoesNotExist:
        return JsonResponse({'state': 'fail', 'error': '客户不存在或无权删除'})
    client.delete()
    return JsonResponse({'state': 'success'})

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """用户信息更新"""
    model = Client
    form_class = ClientForm
    template_name = 'client_update.html'
    success_url = reverse_lazy('client:client_list')
    context_object_name = 'client'

    def get_object(self):
        client = get_object_or_404(Client, owner=self.request.user, pk=self.kwargs.get('pk'))
        return client