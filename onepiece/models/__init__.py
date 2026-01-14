"""
模型层统一导出 - 简化依赖引用
"""
from onepiece.models.database import db, init_db
from onepiece.models.user import User
from onepiece.models.crew_member import CrewMember
from onepiece.models.pirate_group import PirateGroup

__all__ = ['db', 'init_db', 'User', 'CrewMember', 'PirateGroup']
