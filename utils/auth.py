"""
Authentication utilities, JWT tokens and password hashing.
Provides secure password and access token management.
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT settings
SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY", "your-super-secret-jwt-key-change-this-in-production"
)
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes user password using bcrypt.

    Args:
        password (str): Plain text password

    Returns:
        str: Hashed password

    Example:
        >>> hashed = hash_password("MyPassword123")
        >>> print(len(hashed))  # bcrypt hash length
        60
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if plain password matches hashed password.

    Args:
        plain_password (str): Plain text password
        hashed_password (str): Hashed password from database

    Returns:
        bool: True if passwords match, False otherwise

    Example:
        >>> hashed = hash_password("MyPassword123")
        >>> verify_password("MyPassword123", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates JWT access token with expiration time.

    Args:
        data (dict): Data to encode in token
        expires_delta (Optional[timedelta]): Custom expiration time

    Returns:
        str: Encoded JWT token

    Example:
        >>> token = create_access_token({"sub": "user@example.com", "user_id": 1})
        >>> print(token[:20])
        eyJ0eXAiOiJKV1QiLCJh...
    """
    to_encode = data.copy()

    # Set token expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    # Encode token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verifies and decodes JWT token.

    Args:
        token (str): JWT token to verify

    Returns:
        dict: Decoded token data

    Raises:
        HTTPException: If token is invalid or expired

    Example:
        >>> token = create_access_token({"sub": "user@example.com", "user_id": 1})
        >>> payload = verify_token(token)
        >>> print(payload["sub"])
        user@example.com
    """
    try:
        # Decode and verify token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check required fields
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing required fields",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def extract_user_id_from_token(token: str) -> int:
    """
    Extracts user ID from JWT token.

    Args:
        token (str): JWT token

    Returns:
        int: User ID

    Raises:
        HTTPException: If token is invalid or doesn't contain user_id

    Example:
        >>> token = create_access_token({"sub": "user@example.com", "user_id": 1})
        >>> user_id = extract_user_id_from_token(token)
        >>> print(user_id)
        1
    """
    payload = verify_token(token)
    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id
