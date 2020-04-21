from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from oauth.utils import OAuthQQ


class OAuthQQAPIView(APIView):
    def get(self, request):
        """生成ＱＱ登录的地址"""
        state = request.query_params.get('state') # 客户端指定的状态
        oauth = OAuthQQ(state=state)
        url = oauth.get_auth_url()
        print(url)
        return Response(url)
