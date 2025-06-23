"""
Утиліти для аутентифікації, JWT токенів та хешування паролів.
Забезпечує безпечну роботу з паролями та токенами доступу.
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

# Налаштування для JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-this-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Контекст для хешування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хешує пароль користувача за допомогою bcrypt.
    
    Args:
        password (str): Пароль в звичайному тексті
        
    Returns:
        str: Хешований пароль
        
    Example:
        >>> hashed = hash_password("MyPassword123")
        >>> print(len(hashed))  # Довжина хешу bcrypt
        60
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Перевіряє, чи відповідає звичайний пароль хешованому.
    
    Args:
        plain_password (str): Пароль в звичайному тексті
        hashed_password (str): Хешований пароль з бази даних
        
    Returns:
        bool: True якщо паролі збігаються, False інакше
        
    Example:
        >>> hashed = hash_password("MyPassword123")
        >>> verify_password("MyPassword123", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Створює JWT токен доступу з зазначеними даними.
    
    Args:
        data (dict): Дані для включення в токен (зазвичай user_id, email)
        expires_delta (Optional[timedelta]): Час дії токена (за замовчуванням 30 хвилин)
        
    Returns:
        str: JWT токен доступу
        
    Example:
        >>> token = create_access_token({"sub": "user@example.com", "user_id": 1})
        >>> print(type(token))
        <class 'str'>
    """
    to_encode = data.copy()
    
    # Встановлення часу закінчення дії токена
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Кодування токена
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Перевіряє та декодує JWT токен.
    
    Args:
        token (str): JWT токен для перевірки
        
    Returns:
        dict: Декодовані дані з токена
        
    Raises:
        HTTPException: Якщо токен недійсний або закінчився
        
    Example:
        >>> token = create_access_token({"sub": "user@example.com", "user_id": 1})
        >>> payload = verify_token(token)
        >>> print(payload["sub"])
        user@example.com
    """
    try:
        # Декодування та перевірка токена
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Перевірка наявності обов'язкових полів
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недійсний токен: відсутні обов'язкові поля",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Недійсний токен: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def extract_user_id_from_token(token: str) -> int:
    """
    Витягує ID користувача з JWT токена.
    
    Args:
        token (str): JWT токен
        
    Returns:
        int: ID користувача
        
    Raises:
        HTTPException: Якщо токен недійсний або не містить user_id
        
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
            detail="Токен не містить ID користувача",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id 