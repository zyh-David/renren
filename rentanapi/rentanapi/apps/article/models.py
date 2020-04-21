from django.db import models

# Create your models here.
from rentanapi.utils.models import BaseModel
from users.models import User


class ArticleCollection(BaseModel):
    """文集模型"""
    name = models.CharField(max_length=200, verbose_name="文集标题")
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING, verbose_name='用户')

    class Meta:
        db_table = "rr_article_collection"
        verbose_name = "文集"
        verbose_name_plural = verbose_name


class Special(BaseModel):
    """专题模型"""
    name = models.CharField(max_length=200, verbose_name="文章标题")
    image = models.ImageField(null=True, blank=True, verbose_name="封面图片")
    notice = models.TextField(null=True, blank=True, verbose_name="专题公告")
    article_count = models.IntegerField(default=0, null=True, blank=True, verbose_name='文章总数')
    collect_count = models.IntegerField(default=0, null=True, blank=True, verbose_name="关注量")
    follow_count = models.IntegerField(default=0, null=True, blank=True, verbose_name="关注量量")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='创建人')
    class Meta:
        db_table = 'rr_special'
        verbose_name = '专题'
        verbose_name_plural = verbose_name


class Article(BaseModel):
    """文章模型"""
    title = models.CharField(max_length=200, verbose_name="文章标题")
    content = models.TextField(null=True, blank=True, verbose_name="文章内容")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='用户')
    collection = models.ForeignKey(ArticleCollection, on_delete=models.CASCADE, verbose_name='文章')
    pub_date = models.DateTimeField(null=True, default=None, verbose_name='发布时间')
    access_pwd = models.CharField(max_length=15, null=True, blank=True, verbose_name="访问密码")
    read_count = models.IntegerField(default=0, null=True,blank=True,verbose_name="阅读量")
    like_count = models.IntegerField(default=0, null=True, blank=True, verbose_name="点赞量")
    collect_count = models.IntegerField(default=0, null=True, blank=True, verbose_name="收藏量")
    comment_count = models.IntegerField(default=0, null=True, blank=True, verbose_name="评价量")
    reward_count = models.IntegerField(default=0, null=True, blank=True, verbose_name="赞赏量")
    is_public = models.BooleanField(default=False, verbose_name="是否公开")
    save_id = models.IntegerField(default=0, null=True,blank=True, verbose_name='编辑次数')

    class Meta:
        db_table = 'rr_article'
        verbose_name = "文章"
        verbose_name_plural = verbose_name

class ArticlePost(BaseModel):
    """文章的投稿记录"""
    POST_STATUS =(
        (0,'未审核'),
        (1, "审核通过"),
        (2, "审核未通过")
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='投稿人')
    special = models.ForeignKey(Special, on_delete=models.DO_NOTHING, verbose_name='专题')
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, verbose_name='文章')
    status = models.IntegerField(choices=POST_STATUS, default=0, verbose_name='审核状态')
    manager = models.IntegerField(default=None, null=True,blank=True, verbose_name="审核人")
    post_time = models.DateTimeField(default=None, null=True,blank=True, verbose_name="审核时间")

    class Meta:
        db_table = 'rr_article_post'
        verbose_name = '文章的投稿记录'
        verbose_name_plural = verbose_name


class SpecialArticle(BaseModel):
    """文章和专题的绑定关系"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="文章")
    special = models.ForeignKey(Special, on_delete=models.CASCADE, verbose_name="专题")

    class Meta:
        db_table = "rr_special_article"
        verbose_name = "专题的文章"
        verbose_name_plural = verbose_name



class SpecialManager(BaseModel):
    """专题管理员"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="管理员")
    special = models.ForeignKey(Special, on_delete=models.CASCADE, verbose_name="专题")

    class Meta:
        db_table = "rr_special_manager"
        verbose_name = "专题的管理员"
        verbose_name_plural = verbose_name

class SpecialFocus(BaseModel):
    """专题关注"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="管理员")
    special = models.ForeignKey(Special, on_delete=models.CASCADE, verbose_name="专题")

    class Meta:
        db_table = "rr_special_focus"
        verbose_name = "专题的关注"
        verbose_name_plural = verbose_name


class SpecialCollection(BaseModel):
    """专题收藏"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="管理员")
    special = models.ForeignKey(Special, on_delete=models.CASCADE, verbose_name="专题")

    class Meta:
        db_table = "rr_special_collection"
        verbose_name = "专题收藏"
        verbose_name_plural = verbose_name


class ArticleImage(BaseModel):
    """文章图片"""
    group = models.CharField(max_length=15,null=True, blank=True, verbose_name="组名")
    link = models.ImageField(null=True, blank=True, verbose_name="图片地址")

    class Meta:
        db_table = "rr_article_image"
        verbose_name = "文章图片"
        verbose_name_plural = verbose_name