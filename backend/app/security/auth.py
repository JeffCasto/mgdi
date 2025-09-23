"""A stub for an authentication module.

This is a stub for a module that will eventually be used to handle user
authentication and authorization.
"""

def get_current_user(token: str) -> dict:
    """Gets the current user from a JWT token.

    Args:
        token: The JWT token.

    Returns:
        A dictionary with the user's information.
    """
    return {"user_id": "stub"}
