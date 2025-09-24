from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def workflow_endpoint():
    """Workflow endpoint.

    This is a placeholder endpoint for workflows.

    Returns:
        A dictionary with a message indicating that the workflow endpoint was called.
    """
    return {"message": "Workflow endpoint"}
