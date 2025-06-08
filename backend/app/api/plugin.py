from fastapi import APIRouter

router = APIRouter()

@router.post('/')
def plugin_endpoint():
    return {'message': 'Plugin endpoint'}
