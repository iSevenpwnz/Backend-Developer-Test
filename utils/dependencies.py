"""
Dependency Injection functions for FastAPI.
Provide automatic authentication and token validation.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.config import get_db
from models.user import User
from utils.auth import verify_token, extract_user_id_from_token

# HTTP Bearer scheme for automatic token extraction from headers
security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """
    Dependency injection function to get current user ID from token.
    Automatically extracts and validates JWT token from Authorization header.

    Args:
        credentials (HTTPAuthorizationCredentials): JWT token from Authorization header

    Returns:
        int: Authenticated user ID

    Raises:
        HTTPException: If token is invalid or missing

    Example:
        @app.get("/protected")
        def protected_route(user_id: int = Depends(get_current_user_id)):
            return {"user_id": user_id}
    """
    token = credentials.credentials
    return extract_user_id_from_token(token)


def get_current_user(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)
) -> User:
    """
    Dependency injection function to get complete current user information.
    Combines token validation with loading user data from database.

    Args:
        db (Session): Database session
        user_id (int): User ID from token

    Returns:
        User: User object from database

    Raises:
        HTTPException: If user not found or token invalid

    Example:
        @app.get("/profile")
        def get_profile(current_user: User = Depends(get_current_user)):
            return {"email": current_user.email}
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


def validate_token_only(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Dependency injection function for token validation without loading user.
    Used when only token verification is needed without database access.

    Args:
        credentials (HTTPAuthorizationCredentials): JWT token from Authorization header

    Returns:
        dict: Decoded token data

    Raises:
        HTTPException: If token is invalid

    Example:
        @app.get("/token-info")
        def token_info(payload: dict = Depends(validate_token_only)):
            return {"token_payload": payload}
    """
    token = credentials.credentials
    return verify_token(token)


def optional_authentication(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
) -> Optional[int]:
    """
    Dependency injection function for optional authentication.
    Returns user ID if token is present and valid, otherwise None.

    Args:
        credentials (Optional[HTTPAuthorizationCredentials]): Optional JWT token

    Returns:
        Optional[int]: User ID or None if token absent/invalid

    Example:
        @app.get("/public-or-private")
        def mixed_route(user_id: Optional[int] = Depends(optional_authentication)):
            if user_id:
                return {"message": "You are authenticated", "user_id": user_id}
            return {"message": "Public access"}
    """
    if not credentials:
        return None

    try:
        token = credentials.credentials
        return extract_user_id_from_token(token)
    except HTTPException:
        # If token is invalid, return None instead of error
        return None
