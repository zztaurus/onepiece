"""
船员视图 - 船员管理 API
"""
from flask import Blueprint, request
import logging

from onepiece.services import CrewService
from onepiece.utils import success, error, not_found

logger = logging.getLogger(__name__)

crew_bp = Blueprint('crew', __name__)

BLUEPRINT_CONFIG = {
    'blueprint': crew_bp,
    'prefix': '/api/crew'
}


def get_crew_service() -> CrewService:
    """获取船员服务实例"""
    return CrewService()


@crew_bp.route('', methods=['GET'])
def get_all():
    """获取船员列表 GET /api/crew"""
    pirate_group_id = request.args.get('pirate_group_id', type=int)

    service = get_crew_service()
    ok, result, message = service.get_all(pirate_group_id)

    if ok:
        return success(data=result, message=message)
    return error(message)


@crew_bp.route('/<int:member_id>', methods=['GET'])
def get_one(member_id: int):
    """获取船员详情 GET /api/crew/<id>"""
    service = get_crew_service()
    ok, result, message = service.get_by_id(member_id)

    if ok:
        return success(data=result)
    return not_found(message)


@crew_bp.route('', methods=['POST'])
def create():
    """创建船员 POST /api/crew"""
    data = request.get_json() or {}

    service = get_crew_service()
    ok, result, message = service.create(data)

    if ok:
        return success(data=result, message=message), 201
    return error(message)


@crew_bp.route('/<int:member_id>', methods=['PUT'])
def update(member_id: int):
    """更新船员 PUT /api/crew/<id>"""
    data = request.get_json() or {}

    service = get_crew_service()
    ok, result, message = service.update(member_id, data)

    if ok:
        return success(data=result, message=message)
    return not_found(message) if '不存在' in message else error(message)


@crew_bp.route('/<int:member_id>', methods=['DELETE'])
def delete(member_id: int):
    """删除船员 DELETE /api/crew/<id>"""
    service = get_crew_service()
    ok, _, message = service.delete(member_id)

    if ok:
        return success(message=message)
    return not_found(message)


@crew_bp.route('/search', methods=['GET'])
def search():
    """搜索船员 GET /api/crew/search?q=keyword"""
    keyword = request.args.get('q', '')

    service = get_crew_service()
    ok, result, message = service.search(keyword)

    if ok:
        return success(data=result, message=message)
    return error(message)
