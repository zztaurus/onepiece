"""
控制器层 - 蓝图自动发现与注册

新增 controller 步骤：
1. 创建 xxx_controller.py 文件
2. 定义蓝图和 BLUEPRINT_CONFIG
3. 完成！无需修改其他文件
"""
from onepiece.controllers.registry import register_blueprints

__all__ = ['register_blueprints']
