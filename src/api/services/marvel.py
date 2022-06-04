import hashlib
from datetime import datetime
from typing import List, Optional, Set, Tuple

import aiohttp
from requests import HTTPError

from core.config import MARVEL_PRIVATE_KEY, MARVEL_PUBLIC_KEY
from models.character import Character
from models.comic import Comic

MARVEL_BASE_URL = 'https://gateway.marvel.com/v1/public'


def _get_credentials():
    """
    :return: Credential string needed to access Marvel API.
    """
    ts = round(datetime.utcnow().timestamp())
    hash = hashlib.md5(f'{ts}{MARVEL_PRIVATE_KEY}{MARVEL_PUBLIC_KEY}'.encode()).hexdigest()
    return f'apikey={MARVEL_PUBLIC_KEY}&ts={ts}&hash={hash}'


async def _send_get_request(uri: str):
    """
    :param str uri: URI for resource to be fetched.
    :return: Results of requested resource.
    :raise HTTPError: If non 200 response from resource.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            if response.status != 200:
                raise HTTPError(f'Status: {response.status}, URI: {uri}, Reason: {response.reason}')
            return await response.json()


async def get_character_by_id(marvel_id: int) -> Character:
    """
    :param int marvel_id: Marvel API id of the Character to be found.
    :return: The requested Character.
    :raise TypeError: If invalid marvel_id was given as an argument.
    """
    response = await _send_get_request(f'{MARVEL_BASE_URL}/characters/{marvel_id}?{_get_credentials()}')

    if not response['data']['results']:  # Somehow an invalid id was recorded.
        raise TypeError('No Character found for given marvel_id.')

    result = response['data']['results'][0]
    return Character(**{
        'marvel_id': result['id'],
        'comic_count': result['comics']['available'],
        'series_count': result['series']['available'],
        'stories_count': result['stories']['available'],
        'name': result['name'],
        'description': result['description'],
        'thumbnail': f'{result["thumbnail"]["path"]}.{result["thumbnail"]["extension"]}',
    })


async def get_character_by_name(name: str) -> Optional[Character]:
    """
    :param str name: Name of the Character to find.
    :return: The named Character if found.
    """
    response = await _send_get_request(f'{MARVEL_BASE_URL}/characters?name={name}&{_get_credentials()}')

    if not response['data']['results']:
        return None  # Marvel API didn't match a Character to the given Name.

    result = response['data']['results'][0]
    return Character(**{
        'marvel_id': result['id'],
        'comic_count': result['comics']['available'],
        'series_count': result['series']['available'],
        'stories_count': result['stories']['available'],
        'name': result['name'],
        'description': result['description'],
        'thumbnail': f'{result["thumbnail"]["path"]}.{result["thumbnail"]["extension"]}',
    })


async def get_comics_by_character_id(marvel_id: int) -> Tuple[List[Comic], Set[int]]:
    """
    :param int marvel_id: Marvel API id of the Character to be referenced.
    :return: List Comics and affiliated Character marvel_ids
    :raise Exception: exception on http error TODO
    """
    offset = 0
    increment = 20
    uri = f'{MARVEL_BASE_URL}/characters/{marvel_id}/comics?{_get_credentials()}&limit={increment}'
    results = []

    safety_switch = 0  # here for testing so i dont lose api privileges :(
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{uri}&offset={offset}') as response:
                if response.status != 200:
                    # TODO Handle error.
                    raise HTTPError(f'Status: {response.status}, URI: {uri}, Reason: {response.reason}')
                response = await response.json()
                results.extend(response['data']['results'])
                offset += response['data']['count']
                if offset >= response['data']['total']:
                    break
                safety_switch += 1
                if safety_switch > 2:
                    print('Threw the switch!!!!!-------')
                    break

    print('here we are-----')
    print(len(results))
    print(offset)
    print(increment)
    # Organize the results.
    comics: List[Comic] = []
    for result in results:
        url_detail = None  # How unreadable would this be in a comprehension?
        for url in result['urls']:
            if url['type'] == 'detail':
                url_detail = url['url']
                break
        comics.append(Comic(**{
            'marvel_id': result['id'],
            'issue_number': result['issueNumber'],
            'page_count': result['pageCount'],
            'isbn': result['isbn'],
            'title': result['title'],
            'description': result['description'],
            'url_detail': url_detail,
            'thumbnail': f'{result["thumbnail"]["path"]}.{result["thumbnail"]["extension"]}',
        }))
    unique_marvel_ids = {int(item['resourceURI'].split('/')[-1]) for item in result['characters']['items']}
    return comics, unique_marvel_ids
