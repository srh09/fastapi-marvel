from fastapi import APIRouter


router = APIRouter()


@router.get('/api/v1/character')
def get_test():
    return {
        'id': 12345,
        'name': 'Spectrum',
        'description': 'Nice and thorough description of Spectrum',
        'picture': None
    }
