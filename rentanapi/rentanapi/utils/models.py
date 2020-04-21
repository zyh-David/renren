from django.db import models

class BaseModel(models.Model):
    """项目中的公共字段模型"""
    is_show = models.BooleanField(default=False, verbose_name="是否显示")
    orders = models.IntegerField(default=1, verbose_name="排序")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    # auto_now_add 当添加数据时，当前字段使用当前时间戳作为默认值
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # auto_now 当每一次数据发生变化的时候，当前字段都会使用当前时间戳作为默认值
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 设置当前模型为抽象模型，在数据迁移的时候django就不会为它单独创建一张表
        abstract = True