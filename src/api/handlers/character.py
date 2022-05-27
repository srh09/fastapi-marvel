import hashlib
from datetime import datetime

import aiohttp
from fastapi import APIRouter

from env.environment import MARVEL_PRIVATE_KEY, MARVEL_PUBLIC_KEY


router = APIRouter()
# Test Contributions


@router.get('/api/v1/character')
async def get_character():
    # reach out to marvel api to get data
    ts = round(datetime.utcnow().timestamp())
    hash = hashlib.md5(f'{ts}{MARVEL_PRIVATE_KEY}{MARVEL_PUBLIC_KEY}'.encode()).hexdigest()
    name = 'Spectrum'
    uri = f'https://gateway.marvel.com/v1/public/characters?name={name}&apikey={MARVEL_PUBLIC_KEY}&ts={ts}&hash={hash}'

    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            if response.status != 200:
                # TODO Handle error.
                print('There was an error here.')
            response = await response.json()

    return {
        'id': 12345,
        'name': 'Spectrum',
        'description': 'Nice and thorough description of Spectrum',
        'picture': None
    }
