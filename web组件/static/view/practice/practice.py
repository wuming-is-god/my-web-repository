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
from django.views.decorators.http import require_http_methods