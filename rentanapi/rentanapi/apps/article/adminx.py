import xadmin
from .models import Special
class SpecialModelAdmin(object):
    """专题模型管理类"""
    pass
xadmin.site.register(Special, SpecialModelAdmin)


from .models import SpecialArticle
class SpecialArticleModelAdmin(object):
    """专题文章模型管理类"""
    pass
xadmin.site.register(SpecialArticle, SpecialArticleModelAdmin)


from .models import SpecialManager
class SpecialManagerModelAdmin(object):
    """专题管理员模型管理类"""
    pass
xadmin.site.register(SpecialManager, SpecialManagerModelAdmin)