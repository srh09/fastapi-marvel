from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import session
from models.character import Character
from models.comic import Comic
from api.services import marvel

router = APIRouter()


@router.get('/api/v1/comics/character/{marvel_id}')
async def get_comics_by_character(marvel_id: int, db: Session = Depends(session.get_db)):
    main: Character = db.query(Character).filter(Character.marvel_id == marvel_id).first()
    if not main:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Character Not Found.')

    comic_id2comic = {}
    if main.comics_updated:
        # The Comics have already been found for this Character.
        for comic in main.comics:
            comic_id2comic[comic.marvel_id] = comic.to_dict()
    else:
        # Get the Character's Comics from Marvel.
        comics = await marvel.get_comics_by_character_id(main.marvel_id)
        for comic in comics:
            c_db: Comic = db.query(Comic).filter(Comic.marvel_id == comic.marvel_id).first()
            if c_db:  # May already have Comic but still need relationship.
                main.comics.append(c_db)
                comic_id2comic[c_db.marvel_id] = c_db.to_dict()
                continue
            # Discovered a new Comic.
            db.add(comic)
            main.comics.append(comic)
            comic_id2comic[comic.marvel_id] = comic.to_dict()

        main.comics_updated = datetime.now(timezone.utc)
        db.add(main)
        db.commit()

    return comic_id2comic
