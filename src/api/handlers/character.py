from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from db import session
from models.character import Character
from api.services import marvel
from models.comic import Comic

router = APIRouter()


@router.get('/api/v1/character')
async def get_character(name: str, db: Session = Depends(session.get_db)):
    response = {}
    character: Character = db.query(Character).filter(func.lower(Character.name) == name.lower()).first()
    if character:
        response = character.to_dict()
    else:
        character = await marvel.get_character_by_name(name)
        if not character:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Character Not Found.')
        response = character.to_dict()
        db.add(character)
        db.commit()

    return response


@router.get('/api/v1/character/{marvel_id}/affiliates')
async def get_character_affiliates(marvel_id: int, db: Session = Depends(session.get_db)):
    main: Character = db.query(Character).filter(Character.marvel_id == marvel_id).first()
    if not main:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Character Not Found.')
    if not main.comics_updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Must have updated Comics to affiliate.')

    tasks = []
    affiliates = {}
    comic: Comic
    for comic in main.comics:
        if comic.characters_updated:
            # The Characters of this Comic have already been found.
            for character in comic.characters:
                affiliates[character.marvel_id] = character.to_dict()
            continue

        # This Comic's Characters have not been found.  Get them from Marvel.
        tasks.append(marvel.get_characters_by_comic(comic))

    # Speed this up with asyncio concurrent requests.
    results = await marvel.semaphore_gather(tasks, 10)
    for characters, comic in results:
        # Create newly discovered relationships.
        for character in characters:
            c_db: Character = db.query(Character).filter(Character.marvel_id == character.marvel_id).first()
            if c_db:
                comic.characters.append(c_db)
                affiliates[c_db.marvel_id] = c_db.to_dict()
                continue
            # A new Character was discovered.
            print(f'Discovered Character {character.name}-----')
            db.add(character)
            comic.characters.append(character)
            affiliates[character.marvel_id] = character.to_dict()

        comic.characters_updated = datetime.now(timezone.utc)
        db.add(comic)

    db.commit()

    affiliates.pop(marvel_id, None)  # Affiliated with self?  Not for this.

    return affiliates


@router.get('/api/v1/characters/discovered')
async def get_discovered_characters(db: Session = Depends(session.get_db)):
    return [character.to_dict() for character in
            db.query(Character).order_by(desc(Character.created)).limit(40).all()]
