from alipay import AliPay
from django.conf import settings
from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
import random

from article.models import Article
from payments.models import Reward


class AliPayAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_alipay(self):
        app_private_key_string = open(settings.ALIAPY_CONFIG['app_private_key_path']).read()
        alipay_public_key_string = open(settings.ALIAPY_CONFIG['alipay_public_key_path']).read()
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG['appid'],
            app_notify_url=settings.ALIAPY_CONFIG['app_notify_url'],  # 默认的回调url
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type=settings.ALIAPY_CONFIG["sign_type"],
            debug=settings.ALIAPY_CONFIG["debug"]  # 默认False
        )
        return alipay

    def post(self, request):
        """生成支付链接地址"""
        # 创建打赏记录
        user = request.user
        article_id = request.data.get('article_id')
        # 检验用户打赏的文章是否存在
        trade_no = datetime.now().strftime("%Y%m%d%H%M%S") + ('%06d' % user.id) + ("%06d" % random.randint(1,999999))
        reward = Reward.objects.create(
            user=user,
            money=request.data.get('money'),
            article_id=request.data.get('article_id'),
            status=False,
            trade_no=trade_no,
            out_trade_no=None,
            reward_type=request.data.get('type'),
            message=request.data.get('message'),
        )

        if reward.reward_type == 1:
            # 生成支付链接
            # 初始化支付对象
            alipay = self.get_alipay()
            # 调用接口
            order_string = alipay.api_alipay_trade_page_pay(
                out_trade_no=reward.trade_no,
                total_amount=float(reward.money),
                subject='打赏文章',
                return_url=settings.ALIAPY_CONFIG["return_url"],
                notify_url=settings.ALIAPY_CONFIG["notify_url"]
            )
            url = settings.ALIAPY_CONFIG['gateway_url'] + order_string
            print(url)
        else:
            # 进行其他类型的支付方式
            url = ''
        return Response(url)

class AlipayResultAPIView(APIView):
    def get(self, request):
        """同步消息处理"""
        alipay = AliPayAPIView
        data = request.query_params.dict()
        signature = data.pop('sign')
        success = alipay.verify(data, signature)
        if success:
            """支付结果处理"""
            with transaction.atomic():
                save_id = transaction.savepoint()
                try:
                    reward = Reward.objects.get(trade_no=data.get("out_trade_on"))
                    reward.status = True
                    reward.save()

                    article = Article.objects.get(pk=reward.article_id)
                    article.reward_count+=1
                    article.save()

                    # 参考打赏，实现一个资金流水记录【专门显示在线钱包位置】

                    # 给用户增加打赏资金
                    article.user.money+=reward.money
                    article.user.save()
                except:
                    transaction.savepoint_rellback(save_id)
                    return Response({"message":"支付结果处理有误"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({"message":"支付成功！"})
        return Response({'message':"支付失败"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        """异步通知处理"""
        pass
