"""
首页与认证视图 - 管理登录与核心业务
"""
from flask import Blueprint, request, current_app
import logging

from onepiece.services import AuthService
from onepiece.utils import success, unauthorized

logger = logging.getLogger(__name__)

# 定义 index 蓝图（包含认证功能）
index_bp = Blueprint('index', __name__)

# 蓝图配置 - 用于自动注册
BLUEPRINT_CONFIG = {
    'blueprint': index_bp,
    'prefix': '/api/auth'
}


def get_auth_service() -> AuthService:
    """获取认证服务实例"""
    return AuthService(current_app.config['SECRET_KEY'])


@index_bp.route('/login', methods=['POST'])
def login():
    """用户登录 POST /api/auth/login"""
    logger.info('=== login 函数被调用 ===')
    data = request.get_json() or {}
    logger.debug(f'    请求数据: {data}')

    auth_service = get_auth_service()
    ok, result, message = auth_service.login(
        username=data.get('username'),
        password=data.get('password')
    )

    if ok:
        return success(data=result, message=message)
    return unauthorized(message)


@index_bp.route('/verify', methods=['GET'])
def verify():
    """验证token GET /api/auth/verify"""
    token = request.headers.get('Authorization', '')

    auth_service = get_auth_service()
    ok, result, message = auth_service.verify_token(token)

    if ok:
        return success(data=result)
    return unauthorized(message)
