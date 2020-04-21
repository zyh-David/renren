from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    """用户模型类"""
    nickname = models.CharField(max_length=20, null=True, blank=True, verbose_name="用户昵称")
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True, verbose_name="用户头像")
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    money = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="账户余额")
    blocked_money = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="冻结余额")


class Meta:
    db_table = 'rr_users'
    verbose_name = '用户'
    verbose_name_plural = verbose_name