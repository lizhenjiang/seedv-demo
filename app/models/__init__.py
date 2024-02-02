import os
import glob

def register_models():
    models_path = os.path.dirname(__file__)
    model_files = glob.glob(os.path.join(models_path, "*.py"))
    model_modules = [
        os.path.splitext(os.path.basename(model))[0]
        for model in model_files
        if not model.endswith('__init__.py')
    ]

    # 动态导入所有模型模块
    for module in model_modules:
        __import__(f"app.models.{module}")

# 调用register_models来确保所有模型被导入
register_models()