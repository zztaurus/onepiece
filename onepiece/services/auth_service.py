"""
认证服务 - 处理用户认证相关业务逻辑
"""
from datetime import datetime, timedelta
from typing import Optional, Tuple
import jwt
import logging

from onepiece.models.user import User

logger = logging.getLogger(__name__)


class AuthService:
    """认证服务类"""

    def __init__(self, secret_key: str, token_expiry_hours: int = 24):
        self.secret_key = secret_key
        self.token_expiry_hours = token_expiry_hours

    def login(self, username: str, password: str) -> Tuple[bool, Optional[dict], str]:
        """
        用户登录

        Args:
            username: 用户名
            password: 密码

        Returns:
            Tuple[bool, Optional[dict], str]: (成功标志, 数据, 消息)
        """
        logger.info(f'尝试登录: {username}')

        if not username or not password:
            return False, None, '用户名和密码不能为空'

        user = User.find_by_username(username)
        if not user or not user.verify_password(password):
            logger.warning(f'登录失败: {username}')
            return False, None, '用户名或密码错误'

        token = self._generate_token(user.id, username)
        logger.info(f'登录成功: {username}')

        return True, {
            'token': token,
            'user': user.to_dict()
        }, '登录成功'

    def verify_token(self, token: str) -> Tuple[bool, Optional[dict], str]:
        """
        验证 Token

        Args:
            token: JWT token (可包含 Bearer 前缀)

        Returns:
            Tuple[bool, Optional[dict], str]: (成功标志, 用户信息, 消息)
        """
        if not token:
            return False, None, '未提供token'

        # 移除 Bearer 前缀
        if token.startswith('Bearer '):
            token = token[7:]

        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=['HS256']
            )
            return True, {
                'user_id': payload.get('user_id'),
                'username': payload.get('username')
            }, 'token有效'
        except jwt.ExpiredSignatureError:
            return False, None, 'token已过期'
        except jwt.InvalidTokenError:
            return False, None, '无效的token'

    def _generate_token(self, user_id: int, username: str) -> str:
        """生成 JWT Token"""
        return jwt.encode({
            'user_id': user_id,
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=self.token_expiry_hours)
        }, self.secret_key, algorithm='HS256')
