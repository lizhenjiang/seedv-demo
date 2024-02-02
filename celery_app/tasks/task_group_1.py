from celery_app import app
from app.models.apply import Apply
from app.models.process import Process
import asyncio

@app.task
def execute_process(process_id: int):
    async def process_logic():
        # 找到并执行当前Process
        process = await Process.filter(id=process_id).first()
        if process:
            # 执行Process逻辑，示例：
            print(f"Executing process {process_id}")
            # 假设执行逻辑在这里

            # 更新当前Process状态为完成（示例）
            await Process.filter(id=process_id).update(status='completed')

            # 检查是否有child并执行
            if process.child_id:
                execute_process.delay(process.child_id)
            else:
                # 没有下一个Process，将Apply状态更新为完成
                await Apply.filter(id=process.apply_id).update(status='completed')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_logic())

