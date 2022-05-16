from fastapi import APIRouter


router = APIRouter()


@router.get('/')
def get_test():
    return {'message': 'here I am.'}
