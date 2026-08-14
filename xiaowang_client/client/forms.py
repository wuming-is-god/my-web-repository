from django import forms
from .models import Client
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

class ClientForm(forms.ModelForm):
    class Meta:
        model=Client
        fields=['name', 'phone', 'source', 'note']
        widgets = {
            'name':forms.TextInput(attrs={'required':True, 'class':'form-control'}),
            'phone':forms.TextInput(attrs={'required':True, 'class':'form-control'}),
            'source':forms.Select(attrs={'required':True, 'class':'form-select'}),
            'note':forms.Textarea(attrs={'class':'form-control', 'rows':2}),
        }

    def clean_phone(self):
        """验证手机号码格式"""
        phone = self.cleaned_data.get('phone')
        pattern = r'^1[3-9]\d{9}$'
        if not phone:
            raise ValidationError('手机号码不能为空')
        if re.match(pattern, phone):
            return phone
        raise ValidationError('请输入正确的11位手机号码')


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '请输入用户名'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '请输入密码'
        })

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '请输入用户名'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '请输入密码'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '请确认密码'
        })