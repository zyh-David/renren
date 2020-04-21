import re

from rest_framework import serializers

from users.models import User
from .models import ArticleImage, ArticleCollection, Article, Special


class ArticleImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ["link"]

    def create(self, validated_data):
        """保存数据"""
        link = validated_data.get("link")
        instance = ArticleImage.objects.create(link=link)
        instance.group = str(instance.link).split("/")[0]
        instance.save()
        return instance


class ArticleCollectionMidelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCollection
        fields = ['id', 'name']

    def validate(self, attrs):
        name = attrs.get('name')
        user = self.context['request'].user
        try:
            ArticleCollection.objects.get(user=user, name=name)
            raise serializers.ValidationError('此文集名已经创建过')
        except:
            pass

        return attrs

    def create(self, validated_data):
        """保存数据"""
        name = validated_data.get("name")
        user = self.context['request'].user
        instance = ArticleCollection.objects.create(user=user, name=name)

        return instance


class ArticleCollectionDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCollection
        fields = ['name']

    def validate(self, attrs):
        id = self.context['view'].kwargs['pk']
        name = attrs.get('name')
        user = self.context['request'].user
        try:
            ArticleCollection.objects.get(user=user,id=id)
        except ArticleCollection.DoesNotExist:
            raise serializers.ValidationError('当前文集您没有修改权限')
        try:
            ArticleCollection.objects.get(user=user, name=name)
            raise serializers.ValidationError("当前文集没有进行修改或者与您的其他文件同名了！")
        except ArticleCollection.DoesNotExist:
            pass

        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.save()
        return instance


class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'collection', 'save_id']

    def validate(self, attrs):
        content = attrs.get('content')
        if len(content)>0:
            # 判断内容是包含恶意代码，防止客户端遭到跨站脚本攻击[xss]
            content = re.subu("(<)(.*?script.*?)(>)","&lt;\\2&gt;", content )[0]
            # 正则捕获模式，可以提取正则中的小括号里面的内容
            attrs["content"] = content

        return attrs

    def create(self, validated_data):
        instance = Article.objects.create(
            title=validated_data.get("title"),
            content=validated_data.get("content"),
            collection=validated_data.get("collection"),
            user=self.context["request"].user,
            is_public=True,
        )

        return instance


class SpecialModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Special
        fields = ["id","name","image","article_count","follow_count","collect_count","post_status"]


class AuthorMidelSerializer(serializers.ModelSerializer):
    """文章作者"""
    class Meta:
        model = User
        fields = '__all__'


class CollectionInfoModelSerializer(serializers.ModelSerializer):
    """文章信息"""
    class Meta:
        model = ArticleCollection
        fields = '__all__'


class ArticleInfoMidelSerializer(serializers.ModelSerializer):
    user = AuthorMidelSerializer()
    collection = CollectionInfoModelSerializer()
    class Meta:
        model = Article
        fields = [
            "title", "content", "user",
            "collection", "pub_date",
            "read_count", "like_count",
            "collect_count", "comment_count",
            "reward_count",
        ]