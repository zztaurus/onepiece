"""
海贼团模型 - SQLAlchemy ORM
"""
from onepiece.models.database import db
from datetime import datetime


class PirateGroup(db.Model):
    __tablename__ = 'pirate_groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    captain = db.Column(db.String(100), nullable=False)
    ship_name = db.Column(db.String(100))
    total_bounty = db.Column(db.String(50))
    flag_description = db.Column(db.String(200))
    origin = db.Column(db.String(50))
    member_count = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系：一个海贼团有多个船员
    crew_members = db.relationship('CrewMember', backref='pirate_group', lazy='dynamic')

    def __repr__(self):
        return f'<PirateGroup {self.name}>'

    def to_dict(self, include_members=False):
        data = {
            'id': self.id,
            'name': self.name,
            'captain': self.captain,
            'ship_name': self.ship_name,
            'total_bounty': self.total_bounty,
            'flag_description': self.flag_description,
            'origin': self.origin,
            'member_count': self.member_count,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_members:
            data['members'] = [member.to_dict() for member in self.crew_members]

        return data