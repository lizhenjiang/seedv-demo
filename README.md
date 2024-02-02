# SeedV Demo API

## 概述
本项目是一个使用 FastAPI 和 Tortoise ORM 构建的任务管理 API。

## 特性
- 创建具有特定命令和提示词的任务申请（“Apply”）。
- 根据提供的命令类型自动生成一系列流程（“Process”）。
- 跟踪每个流程的状态和结果。
- 检索每个申请及其关联流程的详细信息。

## 表结构
### Apply 表
- `id`: 主键（整数）
- `command`: 命令类型（字符串，最大长度 32）
- `prompt`: 提示词（文本）
- `status`: 整体状态（字符串，最大长度 32，默认为 "pending"）
- `final_result`: 最终结果（JSON格式，可为 null）
- `created_at`: 创建时间（日期时间）
- `updated_at`: 更新时间（日期时间）

### Process 表
- `id`: 主键（整数）
- `apply_id`: 所属 Apply 记录的外键（整数）
- `child_id`: 下一个 Process 的外键（自引用，可为 null）
- `type`: 处理类型（字符串，最大长度 32）
- `status`: 状态（字符串，最大长度 32，默认为 "pending"）
- `sequence`: 执行顺序（整数）
- `result`: 步骤的输出结果（文本，可为 null）
- `input`: 该步骤的输入（文本，可为 null）
- `created_at`: 创建时间（日期时间）
- `updated_at`: 更新时间（日期时间）

## API 端点

### 创建申请
- **POST** `/api/apply`
- 根据提供的命令创建新的申请，并生成一系列流程。

### 获取申请详情
- **GET** `/api/apply/{apply_id}`
- 获取特定申请的详细信息，包括其所有流程。

## 安装和设置

### 需求
- Python 3.11
- FastAPI
- Tortoise ORM
- Celery（用于异步任务处理）