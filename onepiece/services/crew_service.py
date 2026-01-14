"""
船员服务 - 处理船员管理相关业务逻辑
"""
from typing import Optional, Tuple, List
import logging

from onepiece.models.database import db
from onepiece.models.crew_member import CrewMember
from onepiece.models.pirate_group import PirateGroup

logger = logging.getLogger(__name__)


class CrewService:
    """船员服务类"""

    def get_all(self, pirate_group_id: Optional[int] = None) -> Tuple[bool, List[dict], str]:
        """
        获取船员列表

        Args:
            pirate_group_id: 可选，按海贼团筛选

        Returns:
            Tuple[bool, List[dict], str]: (成功标志, 船员列表, 消息)
        """
        try:
            query = CrewMember.query
            if pirate_group_id:
                query = query.filter_by(pirate_group_id=pirate_group_id)

            members = query.order_by(CrewMember.id).all()
            return True, [m.to_dict() for m in members], f'获取到 {len(members)} 名船员'
        except Exception as e:
            logger.error(f'获取船员列表失败: {e}')
            return False, [], '获取船员列表失败'

    def get_by_id(self, member_id: int) -> Tuple[bool, Optional[dict], str]:
        """
        根据 ID 获取船员详情

        Args:
            member_id: 船员 ID

        Returns:
            Tuple[bool, Optional[dict], str]: (成功标志, 船员信息, 消息)
        """
        member = CrewMember.query.get(member_id)
        if not member:
            return False, None, '船员不存在'
        return True, member.to_dict(), '获取成功'

    def create(self, data: dict) -> Tuple[bool, Optional[dict], str]:
        """
        创建船员

        Args:
            data: 船员数据

        Returns:
            Tuple[bool, Optional[dict], str]: (成功标志, 船员信息, 消息)
        """
        # 验证必填字段
        name = data.get('name')
        role = data.get('role')
        bounty = data.get('bounty', '0')

        if not name or not role:
            return False, None, '船员名称和职位不能为空'

        # 验证海贼团是否存在
        pirate_group_id = data.get('pirate_group_id')
        if pirate_group_id:
            group = PirateGroup.query.get(pirate_group_id)
            if not group:
                return False, None, '指定的海贼团不存在'

        try:
            member = CrewMember(
                name=name,
                role=role,
                bounty=bounty,
                image_url=data.get('image_url'),
                description=data.get('description'),
                devil_fruit=data.get('devil_fruit'),
                haki_types=data.get('haki_types'),
                special_skills=data.get('special_skills'),
                signature_moves=data.get('signature_moves'),
                pirate_group_id=pirate_group_id
            )
            db.session.add(member)
            db.session.commit()

            logger.info(f'创建船员成功: {name}')
            return True, member.to_dict(), '创建成功'
        except Exception as e:
            db.session.rollback()
            logger.error(f'创建船员失败: {e}')
            return False, None, '创建船员失败'

    def update(self, member_id: int, data: dict) -> Tuple[bool, Optional[dict], str]:
        """
        更新船员信息

        Args:
            member_id: 船员 ID
            data: 更新数据

        Returns:
            Tuple[bool, Optional[dict], str]: (成功标志, 船员信息, 消息)
        """
        member = CrewMember.query.get(member_id)
        if not member:
            return False, None, '船员不存在'

        # 验证海贼团是否存在
        pirate_group_id = data.get('pirate_group_id')
        if pirate_group_id is not None:
            if pirate_group_id:
                group = PirateGroup.query.get(pirate_group_id)
                if not group:
                    return False, None, '指定的海贼团不存在'

        try:
            # 更新字段
            updatable_fields = [
                'name', 'role', 'bounty', 'image_url', 'description',
                'devil_fruit', 'haki_types', 'special_skills',
                'signature_moves', 'pirate_group_id'
            ]
            for field in updatable_fields:
                if field in data:
                    setattr(member, field, data[field])

            db.session.commit()
            logger.info(f'更新船员成功: {member.name}')
            return True, member.to_dict(), '更新成功'
        except Exception as e:
            db.session.rollback()
            logger.error(f'更新船员失败: {e}')
            return False, None, '更新船员失败'

    def delete(self, member_id: int) -> Tuple[bool, None, str]:
        """
        删除船员

        Args:
            member_id: 船员 ID

        Returns:
            Tuple[bool, None, str]: (成功标志, None, 消息)
        """
        member = CrewMember.query.get(member_id)
        if not member:
            return False, None, '船员不存在'

        try:
            name = member.name
            db.session.delete(member)
            db.session.commit()
            logger.info(f'删除船员成功: {name}')
            return True, None, f'船员 {name} 已删除'
        except Exception as e:
            db.session.rollback()
            logger.error(f'删除船员失败: {e}')
            return False, None, '删除船员失败'

    def search(self, keyword: str) -> Tuple[bool, List[dict], str]:
        """
        搜索船员

        Args:
            keyword: 搜索关键词

        Returns:
            Tuple[bool, List[dict], str]: (成功标志, 船员列表, 消息)
        """
        if not keyword:
            return False, [], '搜索关键词不能为空'

        try:
            members = CrewMember.query.filter(
                db.or_(
                    CrewMember.name.ilike(f'%{keyword}%'),
                    CrewMember.role.ilike(f'%{keyword}%'),
                    CrewMember.devil_fruit.ilike(f'%{keyword}%')
                )
            ).all()
            return True, [m.to_dict() for m in members], f'搜索到 {len(members)} 名船员'
        except Exception as e:
            logger.error(f'搜索船员失败: {e}')
            return False, [], '搜索失败'
