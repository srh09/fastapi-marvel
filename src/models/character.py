from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True, index=True)
    marvel_id = Column(Integer, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    modified = Column(DateTime, nullable=False)
    thumbnail = relationship('Thumbnail', backref='character', uselist=False)
