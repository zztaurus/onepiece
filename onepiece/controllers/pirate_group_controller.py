"""
海贼团控制器 - 海贼团相关接口
"""
from flask import Blueprint
from onepiece.models.pirate_group import PirateGroup
from onepiece.utils import success, not_found, handle_exceptions

pirate_group_bp = Blueprint('pirate_group', __name__)

# 蓝图配置 - 用于自动注册
BLUEPRINT_CONFIG = {
    'blueprint': pirate_group_bp,
    'prefix': '/api/pirate-groups'
}


@pirate_group_bp.route('', methods=['GET'])
@handle_exceptions
def get_groups():
    """获取所有海贼团（不含成员）GET /api/pirate-groups"""
    groups = PirateGroup.query.all()
    return success(data=[g.to_dict() for g in groups])


@pirate_group_bp.route('/<int:id>', methods=['GET'])
@handle_exceptions
def get_group(id):
    """获取海贼团详情（含成员）GET /api/pirate-groups/:id"""
    group = PirateGroup.query.get(id)
    if not group:
        return not_found('海贼团')
    return success(data=group.to_dict(include_members=True))


@pirate_group_bp.route('/<int:id>/members', methods=['GET'])
@handle_exceptions
def get_group_members(id):
    """获取海贼团成员列表 GET /api/pirate-groups/:id/members"""
    group = PirateGroup.query.get(id)
    if not group:
        return not_found('海贼团')
    return success(data=[m.to_dict() for m in group.crew_members])
