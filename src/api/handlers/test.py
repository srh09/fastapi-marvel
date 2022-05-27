from fastapi import APIRouter


router = APIRouter()


@router.get('/api/v1/test')
def get_test():
    return {'message': 'here I am.'}
