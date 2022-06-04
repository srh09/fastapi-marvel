from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import session
from models.character import Character
from api.services import marvel
from models.comic import Comic

router = APIRouter()


@router.get('/api/v1/comics/character/{character_id}')
async def get_comics_by_character(character_id: int, db: Session = Depends(session.get_db)):
    character: Character = db.query(Character).filter(Character.marvel_id == character_id).first()
    if not character.comics_updated:  # Maybe check updated in the last month?
        # Persist all of the Comics that the given Character is related to.
        comics, marvel_ids = await marvel.get_comics_by_character_id(character.marvel_id)
        for comic in comics:
            db_comic: Comic = db.query(Comic).filter(Comic.marvel_id == comic.marvel_id)
            if not db_comic:
                db.add(comic)

        # Persist all unique Characters from related Comics.
        for marvel_id in marvel_ids:
            c: Character = db.query(Character).filter(Character.marvel_id == marvel_id)
            if not c:  # We dont have this Character, get it from Marvel.
                c = await marvel.get_character_by_id(c.marvel_id)
                db.add(c)

        db.commit()

    # Perform Joins to return the comics for the Character and all of the related Characters.
    return {}
