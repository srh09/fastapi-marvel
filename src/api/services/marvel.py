import hashlib
from datetime import datetime
from typing import Dict, Optional

import aiohttp

from core.config import MARVEL_PRIVATE_KEY, MARVEL_PUBLIC_KEY
from models.character import Character
from models.comic import Comic

MARVEL_BASE_URL = 'https://gateway.marvel.com/v1/public'


def get_credentials():
    ts = round(datetime.utcnow().timestamp())
    hash = hashlib.md5(f'{ts}{MARVEL_PRIVATE_KEY}{MARVEL_PUBLIC_KEY}'.encode()).hexdigest()
    return f'apikey={MARVEL_PUBLIC_KEY}&ts={ts}&hash={hash}'


async def get_character_by_name(name) -> Optional[Character]:
    """
    :param str name: Name of the Character to find.
    :return: The named Character if found.
    """
    uri = f'{MARVEL_BASE_URL}/characters?name={name}&{get_credentials()}'

    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            if response.status != 200:
                # TODO Handle error.
                print('character name api error----')
                return None
            response = await response.json()

    if not response['data']['results']:
        return None  # Marvel API didn't match a Character to the given Name.

    result = response['data']['results'][0]
    character = Character(**{
        'marvel_id': result['id'],
        'comic_count': result['comics']['available'],
        'series_count': result['series']['available'],
        'stories_count': result['stories']['available'],
        'name': result['name'],
        'description': result['description'],
        'thumbnail': f'{result["thumbnail"]["path"]}.{result["thumbnail"]["extension"]}',
    })

    return character


async def get_comics_by_character_id(marvel_id) -> Dict:
    """
    :param str marvel_id: Marvel API id of the Character to be referenced.
    :return: Dictionaries containing the Comic and affiliated Character id's
    """
    offset = 0
    increment = 20
    uri = f'{MARVEL_BASE_URL}/{marvel_id}/comics?{get_credentials()}&limit={increment}'
    results = []
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{uri}&offset={offset}') as response:
                if response.status != 200:
                    # TODO Handle error.
                    print('unable to get comics by character_id-------')
                    return []
                response = await response.json()
                results.extend(response['data']['results'])
                offset += response['data']['count']
                if offset >= response['data']['total']:
                    break

    # Organize the results.
    comics = []
    for result in results:
        comics.append(Comic(**{
            'marvel_id': result['id'],
            'issueNumber': result['issueNumber'],
            'page_count': result['page_count'],
            'isbn': result['isbn'],
            'title': result['title'],
            'description': result['description'],
            'url_detail': result['url_detail'],
            'thumbnail': f'{result["thumbnail"]["path"]}.{result["thumbnail"]["extension"]}',
        }))
    unique_character_ids = {int(item.split('/')[-1]) for item in result['characters']['items']}
    return comics, unique_character_ids


async def get_characters_by_comic_id(marvel_id):
    """
    Returns a list of Marvel API Characters by Comic.marvel_id.
    """
    return
