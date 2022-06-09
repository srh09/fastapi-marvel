from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, Table

from db.base_class import Base


character_comic = Table(
    'character_comic',
    Base.metadata,
    Column('comic_id', ForeignKey('comic.id'), primary_key=True),
    Column('character_id', ForeignKey('character.id'), primary_key=True),
    PrimaryKeyConstraint('comic_id', 'character_id')
)
