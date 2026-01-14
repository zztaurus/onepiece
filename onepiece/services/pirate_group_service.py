"""
海贼团服务 - 处理海贼团管理相关业务逻辑
"""
from typing import Optional, Tuple, List
import logging

from onepiece.models.database import db
from onepiece.models.pirate_group import PirateGroup

logger = logging.getLogger(__name__)


class PirateGroupService:
    """海贼团服务类"""

    def get_all(self) -> Tuple[bool, List[dict], str]:
        """
        获取海贼团列表

        Returns:
            Tuple[bool, List[dict], str]: (成功标志, 海贼团列表, 消息)
        """
        try:
            groups = PirateGroup.query.order_by(PirateGroup.id).all()
            return True, [g.to_dict() for g in groups], f'获取到 {len(groups)} 个海贼团'
        except Exception as e:
            logger.error(f'获取海贼团列表失败: {e}')
            return False, [], '获取海贼团列表失败'

    def get_by_id(self, group_id: int, include_members: bool = False) -> Tuple[bool, Optional[dict], str]:
        """
        根据 ID 获取海贼团详情

        Args:
            group_id: 海贼团 ID
            include_members: 是否包含船员列表

        Returns:
            Tuple[bool, Optional[dict], str]: (成功标志, 海贼团信息, 消息)
        """
        group = PirateGroup.query.get(group_id)
        if not group:
            return False, None, '海贼团不存在'
        return True, group.to_dict(include_members=include_members), '获取成功'

    def create(self, data: dict) -> Tuple[bool, Optional[dict], str]:
        """
        创建海贼团

        Args:
            data: 海贼团数据

        Returns:
            Tuple[bool, Optional[dict], str]: (成功标志, 海贼团信息, 消息)
        """
        name = data.get('name')
        captain = data.get('captain')

        if not name or not captain:
            return False, None, '海贼团名称和船长不能为空'

        # 检查名称是否已存在
        existing = PirateGroup.query.filter_by(name=name).first()
        if existing:
            return False, None, f'海贼团 {name} 已存在'

        try:
            group = PirateGroup(
                name=name,
                captain=captain,
                ship_name=data.get('ship_name'),
                total_bounty=data.get('total_bounty', '0'),
                flag_description=data.get('flag_description'),
                origin=data.get('origin'),
                member_count=data.get('member_count', 0),
                description=data.get('description')
            )
            db.session.add(group)
            db.session.commit()

            logger.info(f'创建海贼团成功: {name}')
            return True, group.to_dict(), '创建成功'
        except Exception as e:
            db.session.rollback()
            logger.error(f'创建海贼团失败: {e}')
            return False, None, '创建海贼团失败'

    def update(self, group_id: int, data: dict) -> Tuple[bool, Optional[dict], str]:
        """
        更新海贼团信息

        Args:
            group_id: 海贼团 ID
            data: 更新数据

        Returns:
            Tuple[bool, Optional[dict], str]: (成功标志, 海贼团信息, 消息)
        """
        group = PirateGroup.query.get(group_id)
        if not group:
            return False, None, '海贼团不存在'

        # 检查名称是否与其他海贼团冲突
        new_name = data.get('name')
        if new_name and new_name != group.name:
            existing = PirateGroup.query.filter_by(name=new_name).first()
            if existing:
                return False, None, f'海贼团名称 {new_name} 已被使用'

        try:
            updatable_fields = [
                'name', 'captain', 'ship_name', 'total_bounty',
                'flag_description', 'origin', 'member_count', 'description'
            ]
            for field in updatable_fields:
                if field in data:
                    setattr(group, field, data[field])

            db.session.commit()
            logger.info(f'更新海贼团成功: {group.name}')
            return True, group.to_dict(), '更新成功'
        except Exception as e:
            db.session.rollback()
            logger.error(f'更新海贼团失败: {e}')
            return False, None, '更新海贼团失败'

    def delete(self, group_id: int) -> Tuple[bool, None, str]:
        """
        删除海贼团

        Args:
            group_id: 海贼团 ID

        Returns:
            Tuple[bool, None, str]: (成功标志, None, 消息)
        """
        group = PirateGroup.query.get(group_id)
        if not group:
            return False, None, '海贼团不存在'

        # 检查是否有关联的船员
        if group.crew_members.count() > 0:
            return False, None, f'海贼团 {group.name} 下还有船员，无法删除'

        try:
            name = group.name
            db.session.delete(group)
            db.session.commit()
            logger.info(f'删除海贼团成功: {name}')
            return True, None, f'海贼团 {name} 已删除'
        except Exception as e:
            db.session.rollback()
            logger.error(f'删除海贼团失败: {e}')
            return False, None, '删除海贼团失败'

    def search(self, keyword: str) -> Tuple[bool, List[dict], str]:
        """
        搜索海贼团

        Args:
            keyword: 搜索关键词

        Returns:
            Tuple[bool, List[dict], str]: (成功标志, 海贼团列表, 消息)
        """
        if not keyword:
            return False, [], '搜索关键词不能为空'

        try:
            groups = PirateGroup.query.filter(
                db.or_(
                    PirateGroup.name.ilike(f'%{keyword}%'),
                    PirateGroup.captain.ilike(f'%{keyword}%'),
                    PirateGroup.origin.ilike(f'%{keyword}%')
                )
            ).all()
            return True, [g.to_dict() for g in groups], f'搜索到 {len(groups)} 个海贼团'
        except Exception as e:
            logger.error(f'搜索海贼团失败: {e}')
            return False, [], '搜索失败'

    def get_members(self, group_id: int) -> Tuple[bool, List[dict], str]:
        """
        获取海贼团的所有船员

        Args:
            group_id: 海贼团 ID

        Returns:
            Tuple[bool, List[dict], str]: (成功标志, 船员列表, 消息)
        """
        group = PirateGroup.query.get(group_id)
        if not group:
            return False, [], '海贼团不存在'

        members = [m.to_dict() for m in group.crew_members]
        return True, members, f'{group.name} 共有 {len(members)} 名船员'
