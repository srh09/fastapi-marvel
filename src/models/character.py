from sqlalchemy import Column, DateTime, Integer, String
from db.base_class import Base


class Character(Base):
    id = Column(Integer, primary_key=True, index=True)
    marvel_id = Column(Integer, nullable=False, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)
    modified = Column(DateTime, nullable=False)
