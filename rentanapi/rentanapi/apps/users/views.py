import json
import random
from urllib.parse import urlencode
from urllib.request import urlopen

from django.conf import settings

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from mycelery.sms.yuntongxun.sms import CCP
from rentanapi.settings import constants
from users.models import User
from users.serializer import UserModelSerializer
from mycelery.sms.tasks import send_sms
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from mycelery.mail.tasks import send_email


class CaptchaAPIView(APIView):
    def get(self, request):
        """验证码的验证结果检验"""
        AppSecretKey = settings.TENCENT_CAPTCHA["App_Secret_Key"]
        appid = settings.TENCENT_CAPTCHA["APPID"]
        Ticket = request.query_params.get("ticket")
        Randstr = request.query_params.get("randstr")
        UserIP = request._request.META.get("REMOTE_ADDR")
        print("用户ID地址：%s" % UserIP)
        params = {
            "aid": appid,
            "AppSecretKey": AppSecretKey,
            "Ticket": Ticket,
            "Randstr": Randstr,
            "UserIP": UserIP
        }
        params = urlencode(params)
        f = urlopen("%s?%s" % (settings.TENCENT_CAPTCHA["GATEWAY"], params))
        content = f.read()
        res = json.loads(content)
        print(res)
        if res:
            error_code = res["response"]
            if int(error_code) == 1:
                return Response("验证通过！")
            else:
                return Response("验证失败！%s" % res["err_msg"], status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("验证失败！", status=status.HTTP_400_BAD_REQUEST)


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer



class SMSCodeAPIView(APIView):
    """短信验证码"""
    def get(self, request, mobile):
        # 生成短信验证码
        sms_code = "%06d" % random.randint(0, 999999)

        # 保存短信验证码与发送记录
        redis_conn = get_redis_connection("sms_code")
        # 使用redis提供的管道操作可以一次执行多条redis命令
        pl = redis_conn.pipeline()
        pl.multi()
        pl.setex('sms_%s' % mobile, 300, sms_code)
        pl.setex('sms_time_%s' % mobile, 60, 1)
        pl.execute()

        # 发送短信验证码
        ccp = CCP()
        # ccp.send_template_sms(mobile, [sms_code, "60"], 1)
        send_sms.delay(mobile, sms_code,constants.SMS_INTERVAL_TIME)

        return Response({"message": "OK"}, status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    def get(self, request):
        """发送找回密码的链接地址"""

        # 检测用户是否存在
        email = request.query_params.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('当前邮箱对应的用户不存在！',status=status.HTTP_400_BAD_REQUEST)

        # 生成找回密码的链接
        serializer = Serializer(settings.SECRET_KEY, constants.DATA_SIGNATURE_EXPIRE)
        # dumps的返回值是加密书的bytes信息
        access_token = serializer.dumps({"email": email}).decode()

        url = settings.CLIENT_HOST + "/reset_password?access_token=" + access_token
        print('url', url)

        # 使用dango提供的email发送邮件
        # 使用dango提供的email发送邮件
        send_email.delay([email], url)
        return Response("邮件已经发送，请留意您的邮箱")

    def post(self, request):
        # 验证邮箱链接地址中access_token是否正确并在有效期时间范围内
        access_token = request.data.get('access_token')
        serializer = Serializer(settings.SECRET_KEY, constants.DATA_SIGNATURE_EXPIRE)
        try:
            data = serializer.loads(access_token)
            return Response({'email': data.get('email')})
        except BadData:
            # access_token过期或错误
            return Response('重置密码的邮件已过期或者邮件地址有误！', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # 重置密码
        # 在此从access_token中获取用户信息
        access_token = request.data.get('access_token')
        password = request.data.get('password')
        password2 = request.data.get('password2')

        # 判断密码和确认密码是否一致
        if len(password) < 6 or len(password) >16:
            return Response('密码长度有误！',status=status.HTTP_400_BAD_REQUEST)
        if password != password2:
            return Response('密码和确认密码不一致', status=status.HTTP_400_BAD_REQUEST)
        serializer = Serializer(settings.SECRET_KEY,constants.DATA_SIGNATURE_EXPIRE)
        try:
            data = serializer.loads(access_token)
        except BadData:
            # access_token过期或者错误
            return Response('重置密码的邮件已过期或者邮件地址有误',status=status.HTTP_400_BAD_REQUEST)
        email = data.get('email')
        # 获取用户信息
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response("重置密码失败！邮箱地址有误！", status=status.HTTP_400_BAD_REQUEST)
        # 修改密码
        user.set_password(password)
        user.save()

        return Response('重置密码成功')





