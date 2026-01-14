"""
船员控制器 - 船员相关接口
"""
from flask import Blueprint
from onepiece.models.crew_member import CrewMember
from onepiece.utils import success, not_found, handle_exceptions

crew_bp = Blueprint('crew', __name__)

# 蓝图配置 - 用于自动注册
BLUEPRINT_CONFIG = {
    'blueprint': crew_bp,
    'prefix': '/api/crew'
}


@crew_bp.route('/members', methods=['GET'])
@handle_exceptions
def get_members():
    """获取所有船员 GET /api/crew/members"""
    members = CrewMember.query.all()
    return success(data=[m.to_dict() for m in members])


@crew_bp.route('/members/<int:id>', methods=['GET'])
@handle_exceptions
def get_member(id):
    """获取单个船员 GET /api/crew/members/:id"""
    member = CrewMember.query.get(id)
    if not member:
        return not_found('船员')
    return success(data=member.to_dict())
