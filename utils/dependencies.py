"""
Dependency Injection функції для FastAPI.
Забезпечують автоматичну аутентифікацію та валідацію токенів.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.config import get_db
from models.user import User
from utils.auth import verify_token, extract_user_id_from_token

# HTTP Bearer схема для автоматичного витягування токена з заголовків
security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """
    Dependency injection функція для отримання ID поточного користувача з токена.
    Автоматично витягує та валідує JWT токен з заголовка Authorization.

    Args:
        credentials (HTTPAuthorizationCredentials): JWT токен з заголовка Authorization

    Returns:
        int: ID автентифікованого користувача

    Raises:
        HTTPException: Якщо токен недійсний або відсутній

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
    Dependency injection функція для отримання повної інформації про поточного користувача.
    Комбінує валідацію токена з завантаженням даних користувача з бази даних.

    Args:
        db (Session): Сесія бази даних
        user_id (int): ID користувача з токена

    Returns:
        User: Об'єкт користувача з бази даних

    Raises:
        HTTPException: Якщо користувач не знайдений або токен недійсний

    Example:
        @app.get("/profile")
        def get_profile(current_user: User = Depends(get_current_user)):
            return {"email": current_user.email}
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Користувача не знайдено",
        )

    return user


def validate_token_only(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Dependency injection функція для валідації токена без завантаження користувача.
    Використовується коли потрібно тільки перевірити токен без доступу до бази даних.

    Args:
        credentials (HTTPAuthorizationCredentials): JWT токен з заголовка Authorization

    Returns:
        dict: Декодовані дані з токена

    Raises:
        HTTPException: Якщо токен недійсний

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
    Dependency injection функція для опціональної аутентифікації.
    Повертає ID користувача якщо токен присутній та валідний, інакше None.

    Args:
        credentials (Optional[HTTPAuthorizationCredentials]): Опціональний JWT токен

    Returns:
        Optional[int]: ID користувача або None якщо токен відсутній/недійсний

    Example:
        @app.get("/public-or-private")
        def mixed_route(user_id: Optional[int] = Depends(optional_authentication)):
            if user_id:
                return {"message": "Ви автентифіковані", "user_id": user_id}
            return {"message": "Публічний доступ"}
    """
    if not credentials:
        return None

    try:
        token = credentials.credentials
        return extract_user_id_from_token(token)
    except HTTPException:
        # Якщо токен недійсний, повертаємо None замість помилки
        return None
