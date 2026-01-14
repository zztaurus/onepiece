"""
公共视图 - 通用接口
"""
from flask import Blueprint
from onepiece.utils import success

logger = None

common_bp = Blueprint('common', __name__)

BLUEPRINT_CONFIG = {
    'blueprint': common_bp,
    'prefix': '/api/common'
}

@common_bp.route('/ping', methods=['GET'])
def ping():
    """健康检查"""
    return success(message='pong')

@common_bp.route('/version', methods=['GET'])
def version():
    """获取版本信息"""
    return success(data={'version': '1.0.0'})
