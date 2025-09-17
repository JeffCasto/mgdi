"""A stub for token utilities.

This is a stub for a module that will eventually be used to handle JWT tokens.
"""

def create_token(user_id: str) -> str:
    """Creates a JWT token for a user.

    Args:
        user_id: The ID of the user.

    Returns:
        A JWT token.
    """
    return "stub_token"

def verify_token(token: str) -> str:
    """Verifies a JWT token.

    Args:
        token: The JWT token to verify.

    Returns:
        The user ID from the token.
    """
    return "stub_user_id"
