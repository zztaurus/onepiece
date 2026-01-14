"""
统一响应格式工具 - 最短反馈路径
"""
from flask import jsonify
from functools import wraps


def success(data=None, message=None):
    """成功响应"""
    resp = {'success': True}
    if data is not None:
        resp['data'] = data
    if message:
        resp['message'] = message
    return jsonify(resp)


def error(message, code=400):
    """错误响应"""
    return jsonify({'success': False, 'message': message}), code


def not_found(resource='资源'):
    """404响应"""
    return error(f'{resource}不存在', 404)


def unauthorized(message='未授权'):
    """401响应"""
    return error(message, 401)


def handle_exceptions(f):
    """异常处理装饰器 - 统一捕获异常"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return error(f'服务器错误: {str(e)}', 500)
    return wrapper
