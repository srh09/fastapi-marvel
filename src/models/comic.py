from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Common
from models.relationship import character_comic


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
    characters = relationship('Character', secondary=character_comic, back_populates='comics')

    def to_dict(self):
        return {
            'marvel_id': self.marvel_id,
            'title': self.title,
            'issue_number': self.issue_number,
            'page_count': self.page_count,
            'isbn': self.isbn,
            'description': self.description,
            'url_detail': self.url_detail,
            'thumbnail': self.thumbnail,
        }
