"""
蓝图自动发现与注册器

使用方式：
1. 在 controller 文件中定义蓝图时，添加 BLUEPRINT_CONFIG：

   auth_bp = Blueprint('auth', __name__)
   BLUEPRINT_CONFIG = {
       'blueprint': auth_bp,
       'prefix': '/api/auth'
   }

2. 在 app.py 中调用 register_blueprints(app) 即可自动注册所有蓝图
"""
import os
import importlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def discover_blueprints():
    """
    自动发现 controllers 目录下所有蓝图
    返回: [(blueprint, prefix), ...]
    """
    blueprints = []
    controllers_dir = Path(__file__).parent

    # 扫描所有 *_controller.py 文件
    for file in controllers_dir.glob('*_controller.py'):
        module_name = file.stem  # 如 auth_controller

        try:
            # 动态导入模块
            module = importlib.import_module(f'onepiece.controllers.{module_name}')

            # 检查是否有 BLUEPRINT_CONFIG
            if hasattr(module, 'BLUEPRINT_CONFIG'):
                config = module.BLUEPRINT_CONFIG
                blueprint = config.get('blueprint')
                prefix = config.get('prefix', '')

                if blueprint:
                    blueprints.append((blueprint, prefix))
                    logger.debug(f'发现蓝图: {module_name} -> {prefix}')
            else:
                logger.warning(f'{module_name} 缺少 BLUEPRINT_CONFIG，已跳过')

        except Exception as e:
            logger.error(f'加载 {module_name} 失败: {e}')

    return blueprints


def register_blueprints(app):
    """
    自动注册所有发现的蓝图到 Flask 应用
    """
    blueprints = discover_blueprints()

    for blueprint, prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=prefix)
        logger.info(f'已注册蓝图: {blueprint.name} -> {prefix}')

    logger.info(f'共注册 {len(blueprints)} 个蓝图')
