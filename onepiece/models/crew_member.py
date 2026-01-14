"""
船员模型 - SQLAlchemy ORM
"""
from onepiece.models.database import db
from datetime import datetime


class CrewMember(db.Model):
    __tablename__ = 'crew_members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    role = db.Column(db.String(100), nullable=False)
    bounty = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500))
    description = db.Column(db.Text)
    devil_fruit = db.Column(db.String(200))
    haki_types = db.Column(db.String(200))
    special_skills = db.Column(db.Text)
    signature_moves = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 外键：关联海贼团
    pirate_group_id = db.Column(db.Integer, db.ForeignKey('pirate_groups.id'), nullable=True)

    def __repr__(self):
        return f'<CrewMember {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'bounty': self.bounty,
            'image_url': self.image_url,
            'description': self.description,
            'abilities': {
                'devil_fruit': self.devil_fruit,
                'haki_types': self.haki_types,
                'special_skills': self.special_skills,
                'signature_moves': self.signature_moves
            },
            'pirate_group_id': self.pirate_group_id,
            'pirate_group_name': self.pirate_group.name if self.pirate_group else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }