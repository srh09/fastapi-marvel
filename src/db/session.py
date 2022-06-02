from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import DATABASE_URL


engine = create_engine(DATABASE_URL)
SessionMaker = sessionmaker(bind=engine)


def get_db() -> Generator:
    """
    Starts a new session between the database and application.
    """
    try:
        db = SessionMaker()
        yield db
    finally:
        db.close()
