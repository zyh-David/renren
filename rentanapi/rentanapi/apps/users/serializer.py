import re

from rest_framework import serializers

from users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    '''用户信息序列化器'''
    sms_code = serializers.CharField(required=True, write_only=True, max_length=5, help_text="短信验证码")
    token = serializers.CharField(read_only=True, help_text="jwt登录认证")

    class Meta:
        model = User
        fields = ["id", "username", "mobile", "password", "nickname", "sms_code", "token"]
        extra_kwargs = {
            "id": {"read_only": True, },
            "username": {"read_only": True, },
            "mobile": {"required": True, "write_only": True, },
            "password": {"required": True, "write_only": True, "max_length": 16, "min_length": 6},
            "nickname": {"required": True}
        }

        def validata(self, attrs):
            # 1. 验证手机号码
            mobile = attrs.get('mobile')
            if not re.match("^1[3-9]\d{9}$", mobile):
                raise serializers.ValidationError("手机号码格式错误！")

                # 2. 验证手机号是否注册了
            try:
                User.objects.get(mobile=mobile)
                raise serializers.ValidationError("手机号码被占用！")
            except User.DoesNotExist:
                pass

                # 3. 昵称是否被注册了
            nickname = attrs.get("nickname")
            try:
                User.objects.get(nickname=nickname)
                raise serializers.ValidationError("用户昵称被占用！")
            except User.DoesNotExist:
                pass

            # todo 4. 验证手机短信是否正确

            return attrs

        def create(self, validated_data):
            """保存用户注册信息"""
            mobile = validated_data.get("mobile")
            nickname = validated_data.get("nickname")
            password = validated_data.get("password")
            try:
                user = User.objects.create_user(mobile=mobile, nickname=nickname, password=password)
            except:
                raise serializers.ValidationError("用户信息注册失败！")

            # 返回jwt登录token
            from rest_framework_jwt.settings import api_settings

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            user.token = jwt_encode_handler(payload)

            return user