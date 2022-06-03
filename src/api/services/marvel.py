import hashlib
from datetime import datetime

import aiohttp

from core.config import MARVEL_PRIVATE_KEY, MARVEL_PUBLIC_KEY
from models.character import Character


async def get_api_character_by_name(name):
    """
    Gets Marvel API Character by name.
    """
    ts = round(datetime.utcnow().timestamp())
    hash = hashlib.md5(f'{ts}{MARVEL_PRIVATE_KEY}{MARVEL_PUBLIC_KEY}'.encode()).hexdigest()
    uri = f'https://gateway.marvel.com/v1/public/characters?name={name}&apikey={MARVEL_PUBLIC_KEY}&ts={ts}&hash={hash}'

    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            if response.status != 200:
                # TODO Handle error.
                print('character name api error----')
                return None
            response = await response.json()

    character = None
    if response['data']['results']:
        result = response['data']['results'][0]
        character = Character(**{
            'marvel_id': result['id'],
            'name': result['name'],
            'description': result['description'],
            'modified': result['modified'],
            'thumbnail': f'{result["thumbnail"]["path"]}.{result["thumbnail"]["extension"]}',
        })

    return character
