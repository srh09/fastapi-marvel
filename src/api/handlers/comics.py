from fastapi import APIRouter

from db import session
from models.character import Character
from api.services import marvel

router = APIRouter()


@router.get('/api/v1/comics/character/{character_id}')
async def get_comics_by_character(character_id: int):
    db = session.get_db()
    character: Character = db.query(Character).filter(Character.marvel_id == character_id).first()
    if not character.comics_updated:  # Maybe check updated in the last month?
        # Get the data from api
        comics, ucis = await marvel.get_comics_by_character_id(character.marvel_id)
        # I can link many comics to our character
        # after I can link each of the many comics to their respective characters

    db.commit()
    # return response
