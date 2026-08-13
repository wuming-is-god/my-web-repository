from django.db import models
from django.contrib.auth.models import User

SOURCE = [('web', '官网'), ('referral', '转介绍'), ('cold_call', '电话陌拜'), ('other', '其他')]


class Client(models.Model):
    name = models.CharField(max_length=50, verbose_name='客户名')
    phone = models.CharField(max_length=20, verbose_name='手机号码')
    source = models.CharField(max_length=20, choices=SOURCE, verbose_name='来源')
    note = models.TextField(blank=True, default='', verbose_name='备注')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients',
      verbose_name='外键')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='填写时间')

    class Meta:
        db_table = 'tb_client'
        verbose_name = '客户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name