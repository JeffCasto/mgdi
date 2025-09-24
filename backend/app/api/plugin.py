from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def plugin_endpoint():
    """Plugin endpoint.

    This is a placeholder endpoint for plugins.

    Returns:
        A dictionary with a message indicating that the plugin endpoint was called.
    """
    return {"message": "Plugin endpoint"}
