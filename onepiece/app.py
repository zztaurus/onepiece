from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from onepiece.config import Config
from onepiece.models import db, init_db
from onepiece.controllers.registry import register_blueprints
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """应用工厂函数"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(Config)

    # 初始化CORS
    # CORS(app)

    # 初始化数据库
    db.init_app(app)


    # 自动发现并注册所有蓝图
    register_blueprints(app)

    # 请求前日志 - 记录每个进入的请求
    @app.before_request
    def log_request_info():
        logger.info(f'>>> 收到请求: {request.method} {request.path}')
        logger.debug(f'    Headers: {dict(request.headers)}')
        logger.debug(f'    匹配的端点: {request.endpoint}')

    # 全局错误处理（最短反馈路径）
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'success': False, 'message': '接口不存在'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500

    @app.errorhandler(405)
    def method_not_allowed(e):
        logger.error(f'!!! 405错误: {request.method} {request.path}')
        logger.error(f'    允许的方法: {e.valid_methods}')
        return jsonify({'success': False, 'message': '请求方法不允许'}), 405

    # 创建表和初始化数据
    with app.app_context():
        init_db()

    # 打印所有注册的路由
    logger.info('=== 已注册的路由 ===')
    for rule in app.url_map.iter_rules():
        logger.info(f'    {rule.rule} -> {rule.endpoint} [{", ".join(rule.methods)}]')

    return app


if __name__ == '__main__':
    app = create_app()

    print("=" * 70)
    print("🏴‍☠️ Flask MVC服务器启动成功！(SQLAlchemy ORM版本)")
    print("=" * 70)
    print(f"📍 访问地址: http://localhost:8080")
    print(f"🗄️  数据库: MySQL - {app.config['MYSQL_DATABASE']}")
    print(f"👤 测试账号: admin/admin123 或 user/user123")
    print("=" * 70)

    app.run(host='0.0.0.0', debug=True, port=8080)