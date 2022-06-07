from sqlalchemy import Column, DateTime, Integer, func

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Common(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    updated = Column(DateTime(timezone=True), nullable=False, index=True, server_default=func.now(),
                     onupdate=func.now())
    created = Column(DateTime(timezone=True), nullable=False, index=True, server_default=func.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    # def to_dict(self):
    #     d = self.__dict__.copy()
    #     d.pop('_sa_instance_state', None)
    #     return d
