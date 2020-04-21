from django.db import models

from article.models import Article
from rentanapi.utils.models import BaseModel
from users.models import User


class Reward(BaseModel):
    REWARD_TYPE = (
        (1,'支付宝'),
        (2, '余额'),
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='用户')
    money = models.DecimalField(decimal_places=2, max_digits=6, verbose_name='打赏金额')
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, verbose_name="文章")
    status = models.BooleanField(default=False, verbose_name="是否支付")
    trade_no = models.CharField(max_length=255, null=True, blank=True, verbose_name='流水账号')
    out_trade_no = models.CharField(max_length=255, null=True, blank=True, verbose_name="支付宝流水账号")
    reward_type = models.IntegerField(choices=REWARD_TYPE, default=1, verbose_name='支付方式')
    message = models.TextField(null=True, blank=True, verbose_name="留言")

    class Meta:
        db_table = 'rr_user_reward'
        verbose_name = '打赏记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nickname + "打赏了" + self.article.user.nickname + "的文章《" + self.article.title + "》" + self.money + "元"
