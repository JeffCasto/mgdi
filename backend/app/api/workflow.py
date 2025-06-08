from fastapi import APIRouter

router = APIRouter()

@router.post('/')
def workflow_endpoint():
    return {'message': 'Workflow endpoint'}
