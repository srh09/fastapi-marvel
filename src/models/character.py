from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from db.base_class import Common
from models.relationship import character_comic


class Character(Common):
    __tablename__ = 'character'
    marvel_id = Column(Integer, nullable=False, index=True)
    comic_count = Column(Integer, nullable=False)
    series_count = Column(Integer, nullable=False)
    stories_count = Column(Integer, nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    thumbnail = Column(String, nullable=False)
    comics_updated = Column(DateTime)
    comics = relationship('Comic', secondary=character_comic, back_populates='characters')

    def to_dict(self):
        return {
            'marvel_id': self.marvel_id,
            'name': self.name,
            'comic_count': self.comic_count,
            'series_count': self.series_count,
            'stories_count': self.stories_count,
            'description': self.description,
            'thumbnail': self.thumbnail,
        }
