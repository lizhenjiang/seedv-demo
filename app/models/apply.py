from tortoise.models import Model
from tortoise import fields

class Apply(Model):
    id = fields.IntField(pk=True, description="主键")
    command = fields.CharField(max_length=32, description="命令类型")
    prompt = fields.TextField(description="提示词")
    status = fields.CharField(max_length=32, description="整体状态", default="pending")
    final_result = fields.JSONField(description="最终结果", null=True)  # 增加的JSON格式字段
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
