from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from db import session
from models.character import Character
from api.services import marvel

router = APIRouter()


@router.get('/api/v1/character')
async def get_character(db: Session = Depends(session.get_db),
                        name: str = Query(..., description="get a character")):
    print('getting the character-----')
    character: Character = db.query(Character).filter(func.lower(Character.name) == name.lower()).first()
    if not character:
        character = await marvel.get_api_character_by_name(name)
        if not character:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Character Not Found.')
        db.add(character)

    response = character.to_dict()
    db.commit()
    return response
