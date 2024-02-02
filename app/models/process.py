from tortoise.models import Model
from tortoise import fields

class Process(Model):
    id = fields.IntField(pk=True, description="主键")
    apply = fields.ForeignKeyField("models.Apply", related_name="processes", description="所属Apply记录")
    child = fields.ForeignKeyField('models.Process', related_name='parent', null=True, description="下一个Process")  # 自引用外键
    type = fields.CharField(max_length=32, description="处理类型")
    status = fields.CharField(max_length=32, description="状态", default="pending")
    sequence = fields.IntField(description="执行顺序")
    result = fields.TextField(description="步骤的输出结果", null=True)
    input = fields.TextField(description="该步骤的输入", null=True)
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")