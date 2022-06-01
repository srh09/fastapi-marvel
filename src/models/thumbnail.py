from sqlalchemy import Column, ForeignKey, Integer, String
from db.base_class import Base


class Thumbnail(Base):
    __tablename__ = 'thumbnail'
    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey('character.id'), nullable=False)
    path = Column(String, nullable=False)
    extension = Column(String, nullable=False)
