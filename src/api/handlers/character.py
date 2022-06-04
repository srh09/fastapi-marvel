from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func

from db import session
from models.character import Character
from api.services import marvel

router = APIRouter()


@router.get('/api/v1/character')
async def get_character(name: str):
    db = session.get_db()
    character: Character = db.query(Character).filter(func.lower(Character.name) == name.lower()).first()
    if not character:
        character = await marvel.get_character_by_name(name)
        if not character:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Character Not Found.')
        db.add(character)

    response = character.to_dict()  # Must retrieve data from object before commit.
    db.commit()
    return response
