from typing import Any

from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    id: Any
    __name__: str

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
