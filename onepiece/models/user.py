"""
用户模型 - SQLAlchemy ORM
"""
from onepiece.models.database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def find_by_username(cls, username):
        """根据用户名查找用户"""
        return cls.query.filter_by(username=username).first()

    def verify_password(self, password):
        """验证密码"""
        return self.password == password