from fastapi import APIRouter, HTTPException

from ..models.apply import Apply
from ..models.process import Process
from ..schemas.apply import ApplyRequest, ApplyResponse
from ..schemas.process import ApplyDetailedResponse, ProcessResponse
from tortoise.transactions import in_transaction
from celery_app.tasks.task_group_1 import execute_process

router = APIRouter(prefix="/api", tags=["任务相关接口"])

@router.post("/apply", response_model=ApplyResponse)
async def create_apply(request: ApplyRequest):
    async with in_transaction() as conn:
        # 创建Apply记录
        apply = await Apply.create(
            command=request.command,
            prompt=request.prompt,
            using_db=conn  # 使用事务连接
        )

        process_sequence = {
            "command1": ["text_search", "text_to_speech", "text_to_image", "image_to_video"],
            "command2": ["text_search", "text_to_image", "text_to_speech"]
        }

        if request.command not in process_sequence:
            raise HTTPException(status_code=400, detail="Invalid command")

        sequence = 1
        previous_process_id = None
        for process_type in process_sequence[request.command]:
            process = await Process.create(
                apply_id=apply.id,
                type=process_type,
                sequence=sequence,
                using_db=conn  # 使用事务连接
            )
            if previous_process_id is not None:
                await Process.filter(id=previous_process_id).update(child_id=process.id)
            previous_process_id = process.id
            sequence += 1

        # 找到并开始执行第一个Process
        if sequence > 0:  # 确保至少创建了一个Process
            first_process_id = await Process.filter(apply_id=apply.id, sequence=1).first()
            if first_process_id:
                execute_process.delay(first_process_id.id)  # 异步执行第一个Process

        return ApplyResponse(id=apply.id, command=apply.command, status=apply.status)

@router.get("/apply/{apply_id}", response_model=ApplyDetailedResponse)
async def get_apply(apply_id: int):
    # 查询Apply记录
    apply = await Apply.filter(id=apply_id).prefetch_related("processes").first()
    if not apply:
        raise HTTPException(status_code=404, detail="Apply not found")

    # 从Apply实例中获取processes，并转换为ProcessResponse模型列表
    processes_responses = [ProcessResponse(
        id=process.id,
        type=process.type,
        status=process.status,
        sequence=process.sequence,
        result=process.result
    ) for process in apply.processes]

    # 返回包括Apply信息和所有相关Process信息的响应
    return ApplyDetailedResponse(
        id=apply.id,
        command=apply.command,
        status=apply.status,
        processes=processes_responses
    )
