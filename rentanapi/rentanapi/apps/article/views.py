from datetime import datetime

from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import ArticleImage, ArticleCollection, Article, Special, SpecialArticle
from .serializer import ArticleImageModelSerializer, ArticleCollectionMidelSerializer, \
    ArticleCollectionDetailModelSerializer, ArticleModelSerializer, SpecialModelSerializer, ArticleInfoMidelSerializer


class ImageAPIView(CreateAPIView):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageModelSerializer


class CollecionAPIView(CreateAPIView, ListAPIView):
    """文集的视图接口"""
    queryset = ArticleCollection.objects.all()
    serializer_class = ArticleCollectionMidelSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request,  *args, **kwargs):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset().filter(user=user))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CollecionDetailAPIView(UpdateAPIView):
    queryset = ArticleCollection.objects.all()
    serializer_class = ArticleCollectionDetailModelSerializer
    permission_classes = [IsAuthenticated]


class ArticleAPIView(ModelViewSet):
    """文章的视图集接口"""
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["PUT"], detail=True)
    def save_article(self, request, pk):
        # 接收文章内容,　标题,编辑次数,文章id
        content = request.data.get('content')
        title = request.data.get('title')
        save_id = request.data.get('save_id')
        collection_id = request.data.get('collection_id')
        user = request.user

        if save_id is None:
            save_id = 1

        else:
            save_id +=1

        # 验证文章是否存在
        try:
            article = Article.objects.get(user=user, pk=pk)
        except Article.DoesNotExist:
            return Response({'message': "当前文章不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        # 写入redis
        redis_conn = get_redis_connection('article')
        new_timestamp = datetime.now().timestamp()
        data = {
            'title': title,
            'content': content,
            'updated_time':new_timestamp,
            "collection": collection_id
        }
        redis_conn.hmset('article_%s_%s_%s' % (user.id, pk, save_id), data)
        redis_conn.hset("article_history_%s" % (user.id), pk, save_id)

        return Response({'message': "保存成功", "save_id": save_id})

    def list(self, request, *args, **kwargs):
        user = request.user
        collection_id = request.query_params.get("collection")
        try:
            ArticleCollection.objects.get(user=user, id=collection_id)
        except ArticleCollection.DoesNotExist:
            return Response({"message": '对不起，文集不存在'})
        # 先到redis中查询
        redis_conn = get_redis_connection('article')
        history_dist = redis_conn.hgetall('article_history_%s' % user.id)
        data = []
        print(history_dist)
        exclude_id = []
        if history_dist is not None:
            for article_id, save_id in history_dist.items():
                article_id = article_id.decode()
                save_id = save_id.decode()
                article_data_byte = redis_conn.hgetall('article_%s_%s_%s' % (user.id, article_id, save_id))
                data.append({
                    "id": article_id,
                    "title": article_data_byte["title".encode()].decode(),
                    "content": article_data_byte["content".encode()].decode(),
                    "save_id": save_id,
                    "collection": collection_id,
                })
                exclude_id.append(article_id)
        print(data)
        # 查询出除去redis中编辑过的mysql中的数据
        queryset = self.filter_queryset(self.get_queryset().filter(user=user, collection_id=collection_id).exclude(id__in=exclude_id) )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        data += serializer.data
        return Response(data)


    @action(methods=['patch'],detail=True)
    def pub_article(self,request,pk):
        """发布文章"""
        user = request.user
        status = request.data.get('is_pub')

        try:
            article = Article.objects.get(user=user, pk=pk)
        except:
            return Response({"message": "当前文章不存在或者您没有修改的权限！"})

        if status:
            """发布文章"""
            article.pub_date = datetime.now()
            message = {"message": "发布文章成功"}
        else:
            """取消发布"""
            article.pub_date = None
            message = {'message': "取消发布成功"}

        # 从redis的编辑记录中提取当前文章的最新记录
        redis_conn = get_redis_connection("article")
        user_history_dist = redis_conn.hgetall("article_history_%s" % user.id)
        save_id = user_history_dist.get(pk.encode()).decode()
        article_dict = redis_conn.hgetall('article_%s_%s_%s*' % (user.id, pk, save_id))
        print(article_dict)
        if article_dict:
            article.title = article_dict['title'].decode()
            article.content = article_dict['content'.encode()].decode()
            timestamp = datetime.fromtimestamp(int(float(article_dict["updated_time".encode()].decode())))
            article.updated_time = timestamp
            article.save_id = save_id
        article.save()

        return Response(message)

    @action(methods=['patch'], detail=True)
    def change_collection(self, request, pk):
        """切换当前文章的文集ID"""
        user = request.user
        collection_id = request.data.get('cillection_id')
        try:
            article = Article.objects.get(user=user,pk=pk)
        except:
            return Response({"message": "当前文章不存在或者您没有修改的权限！"})

        try:
            ArticleCollection.objects.get(user=user, pk=collection_id)
        except:
            return Response({"message": "当前文集不存在或者您没有修改的权限！"})

        # 当前文章如果之前有曾经被编辑，则需要修改redis中的缓存
        redis_conn = get_redis_connection('article')
        save_id_bytes = redis_conn.hget('article_histor_%s' % (user.id), pk)
        if save_id_bytes is not None:
            save_id = save_id_bytes.decode()
            redis_conn.hset("article_%s_%s_%s" % (user.id, pk, save_id ), "collection_id",   collection_id )
        article.collection_id = collection_id
        article.save()

        return Response({"message":"切换文章的文集成功！"})


class SpecialListAPIView(ListAPIView):
    queryset = Special.objects.all()
    serializer_class = SpecialModelSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        ret = self.get_queryset().filter(mymanager__user=user)
        article_id = request.query_params.get('article_id')

        queryset = self.filter_queryset(ret)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # # 返回专题对于当前文章的收录状态
        data = []
        for special in serializer.data:
            try:
                SpecialArticle.objects.get(article_id=article_id, special_id=special.get("id"))
                special["post_status"] = True # 表示当前文章已经被专题收录了
            except SpecialArticle.DoesNotExist:
                special["post_status"] = False  # 表示当前文章已经被专题收录了
            data.append(special)

            return Response(serializer.data)


class ArticleInfoAPIView(RetrieveAPIView):
    serializer_class = ArticleInfoMidelSerializer
    queryset = Article.objects.all()



