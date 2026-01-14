"""
认证控制器 - 登录、验证
"""
from flask import Blueprint, request, current_app
from datetime import datetime, timedelta
import jwt
import logging
from onepiece.models.user import User
from onepiece.utils import success, unauthorized

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

# 蓝图配置 - 用于自动注册
BLUEPRINT_CONFIG = {
    'blueprint': auth_bp,
    'prefix': '/api/auth'
}


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录 POST /api/auth/login"""
    logger.info('=== login 函数被调用 ===')
    data = request.get_json() or {}
    logger.debug(f'    请求数据: {data}')
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return unauthorized('用户名和密码不能为空')

    user = User.find_by_username(username)
    if not user or not user.verify_password(password):
        return unauthorized('用户名或密码错误')

    token = jwt.encode({
        'user_id': user.id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return success(
        data={'token': token, 'user': user.to_dict()},
        message='登录成功'
    )


@auth_bp.route('/verify', methods=['GET'])
def verify():
    """验证token GET /api/auth/verify"""
    token = request.headers.get('Authorization', '')

    if not token:
        return unauthorized('未提供token')

    if token.startswith('Bearer '):
        token = token[7:]

    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return success(data={
            'user_id': payload.get('user_id'),
            'username': payload.get('username')
        })
    except jwt.ExpiredSignatureError:
        return unauthorized('token已过期')
    except jwt.InvalidTokenError:
        return unauthorized('无效的token')
