"""
海贼团视图 - 海贼团管理 API
"""
from flask import Blueprint, request
import logging

from onepiece.services import PirateGroupService
from onepiece.utils import success, error, not_found

logger = logging.getLogger(__name__)

pirate_group_bp = Blueprint('pirate_group', __name__)

BLUEPRINT_CONFIG = {
    'blueprint': pirate_group_bp,
    'prefix': '/api/pirate-groups'
}


def get_pirate_group_service() -> PirateGroupService:
    """获取海贼团服务实例"""
    return PirateGroupService()


@pirate_group_bp.route('', methods=['GET'])
def get_all():
    """获取海贼团列表 GET /api/pirate-groups"""
    service = get_pirate_group_service()
    ok, result, message = service.get_all()

    if ok:
        return success(data=result, message=message)
    return error(message)


@pirate_group_bp.route('/<int:group_id>', methods=['GET'])
def get_one(group_id: int):
    """获取海贼团详情 GET /api/pirate-groups/<id>"""
    include_members = request.args.get('include_members', 'false').lower() == 'true'

    service = get_pirate_group_service()
    ok, result, message = service.get_by_id(group_id, include_members=include_members)

    if ok:
        return success(data=result)
    return not_found(message)


@pirate_group_bp.route('', methods=['POST'])
def create():
    """创建海贼团 POST /api/pirate-groups"""
    data = request.get_json() or {}

    service = get_pirate_group_service()
    ok, result, message = service.create(data)

    if ok:
        return success(data=result, message=message), 201
    return error(message)


@pirate_group_bp.route('/<int:group_id>', methods=['PUT'])
def update(group_id: int):
    """更新海贼团 PUT /api/pirate-groups/<id>"""
    data = request.get_json() or {}

    service = get_pirate_group_service()
    ok, result, message = service.update(group_id, data)

    if ok:
        return success(data=result, message=message)
    return not_found(message) if '不存在' in message else error(message)


@pirate_group_bp.route('/<int:group_id>', methods=['DELETE'])
def delete(group_id: int):
    """删除海贼团 DELETE /api/pirate-groups/<id>"""
    service = get_pirate_group_service()
    ok, _, message = service.delete(group_id)

    if ok:
        return success(message=message)
    if '不存在' in message:
        return not_found(message)
    return error(message)


@pirate_group_bp.route('/search', methods=['GET'])
def search():
    """搜索海贼团 GET /api/pirate-groups/search?q=keyword"""
    keyword = request.args.get('q', '')

    service = get_pirate_group_service()
    ok, result, message = service.search(keyword)

    if ok:
        return success(data=result, message=message)
    return error(message)


@pirate_group_bp.route('/<int:group_id>/members', methods=['GET'])
def get_members(group_id: int):
    """获取海贼团船员 GET /api/pirate-groups/<id>/members"""
    service = get_pirate_group_service()
    ok, result, message = service.get_members(group_id)

    if ok:
        return success(data=result, message=message)
    return not_found(message)
