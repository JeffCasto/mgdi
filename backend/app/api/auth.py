from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
def login():
    """Logs in a user.

    This is a placeholder endpoint for logging in a user.

    Returns:
        A dictionary with a message indicating that the login endpoint was called.
    """
    return {"message": "Login endpoint"}
