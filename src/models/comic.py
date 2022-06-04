from sqlalchemy import Column, Integer, String

from db.base_class import Common


class Comic(Common):
    __tablename__ = 'comic'
    marvel_id = Column(Integer, nullable=False, index=True)
    issue_number = Column(Integer, nullable=False)
    page_count = Column(Integer, nullable=False)
    isbn = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    url_detail = Column(String, nullable=False)
    thumbnail = Column(String, nullable=False)
    # characters = relationship('Character', secondary=character_comic, back_populates='comics')
