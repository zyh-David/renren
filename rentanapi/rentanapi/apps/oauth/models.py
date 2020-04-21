from django.db import models
from rentanapi.utils.models import BaseModel
# Create your models here.
from users.models import User


class OAuthUser(BaseModel):
    """
        登录用户数据
        """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'rr_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name