from celery import Celery
# 初始化celery对象
app = Celery("luffy")

# 如果想要在celery中执行django的代码，例如模型操作，日志记录，则必须在当前celery中对django进行初始化
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rentanapi.settings.dev')
import django
django.setup()

# 加载在config里面编写的配置信息
app.config_from_object("mycelery.config")

# 编写celery的任务[各个任务目录的tasks文件中编写]

# 在main当前文件中，注册任务到celery
# 自动搜索并加载任务
# 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称
# app.autodiscover_tasks(["任务1","任务2"])
app.autodiscover_tasks(["mycelery.mail","mycelery.sms"])


# 在终端下启动celery，必须在mycelery的父级目录下运行
# celery -A mycelery.main worker --loglevel=info
