import hashlib
from datetime import datetime

import aiohttp
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import session
from core.config import MARVEL_PRIVATE_KEY, MARVEL_PUBLIC_KEY
from models.character import Character


router = APIRouter()
# Test Contributions


@router.get('/api/v1/character')
async def get_character(
    db: Session = Depends(session.get_db)
):
    # reach out to marvel api to get data
    ts = round(datetime.utcnow().timestamp())
    hash = hashlib.md5(f'{ts}{MARVEL_PRIVATE_KEY}{MARVEL_PUBLIC_KEY}'.encode()).hexdigest()
    name = 'Spectrum'
    uri = f'https://gateway.marvel.com/v1/public/characters?name={name}&apikey={MARVEL_PUBLIC_KEY}&ts={ts}&hash={hash}'

    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            if response.status != 200:
                # TODO Handle error.
                raise Exception('There was an error here.')
            response = await response.json()

    result = response['data']['results'][0]
    character: Character = db.query(Character).filter(Character.marvel_id == result['id']).first()
    if not character:
        character = Character()
    character.update(**{
        'marvel_id': result['id'],
        'name': result['name'],
        'description': result['description'],
        'modified': result['modified']
    })
    db.add(character)
    db.commit()

    return {
        'id': character.marvel_id,
        'name': character.name,
        'description': character.description,
        'picture': None
    }
