from sqlalchemy import Column, Integer, String, DateTime

from db.base_class import Common


# character_comic = Table(
#     'character_comic',
#     Base.metadata,
#     Column('comic_id', ForeignKey('comic.id'), primary_key=True),
#     Column('character_id', ForeignKey('character.id'), primary_key=True),
# )


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
    # comics = relationship('Comic', secondary=character_comic, back_populates='characters')
