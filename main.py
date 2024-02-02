from fastapi import FastAPI
from app.api.task_router import router as task_router
from tortoise.contrib.fastapi import register_tortoise
from config.config import DATABASE_CONFIG
from celery_app import app as celery_app  # 重命名导入的 Celery 实例

app = FastAPI()

# 注册Tortoise ORM
register_tortoise(
    app,
    config=DATABASE_CONFIG,
    generate_schemas=True,  # 自动生成表结构，生产环境需关闭
    add_exception_handlers=True # 生产环境需关闭
)

app.include_router(task_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
