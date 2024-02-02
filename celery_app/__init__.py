from celery import Celery
from tortoise import Tortoise
import asyncio
from config.config import DATABASE_CONFIG


app = Celery('seedv-demo')
app.config_from_object('celery_app.celery_config')

# Tortoise ORM 初始化函数
# async def init_tortoise():
#     await Tortoise.init(
#         db_url=DATABASE_CONFIG['connections']['default'],
#         modules={'models': ['app.models.apply','app.models.process']}
#     )
#     await Tortoise.generate_schemas()
#
# # 使用事件循环同步地调用异步初始化函数
# loop = asyncio.get_event_loop()
# loop.run_until_complete(init_tortoise())

from celery.signals import worker_init, worker_shutdown
@worker_init.connect
def init_tortoise(sender=None, conf=None, **kwargs):
    Tortoise.init(
        db_url=DATABASE_CONFIG['connections']['default'],
        modules={'models': ['app.models']}
    )
    Tortoise.generate_schemas()
#
# 确保在 Celery worker 关闭时关闭 ORM
@worker_shutdown.connect
def shutdown_tortoise(sender=None, conf=None, **kwargs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Tortoise.close_connections())

# 导入任务
from celery_app.tasks.example_task import add
from celery_app.tasks.task_group_1 import execute_process

# 手动注册任务
app.task(add)
app.task(execute_process)


# 自动发现任务
# app.autodiscover_tasks(['celery_app.tasks'])