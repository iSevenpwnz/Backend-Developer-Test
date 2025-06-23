"""
Контролер аутентифікації.
Містить ендпоінти для реєстрації та авторизації користувачів.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from schemas.user import UserSignup, UserLogin, TokenResponse, UserResponse
from services.user_service import UserService

# Створення роутера для аутентифікації
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/signup",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    user_data: UserSignup, db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Реєстрація нового користувача в системі.

    Args:
        user_data (UserSignup): Дані для реєстрації (email, password)
        db (Session): Сесія бази даних

    Returns:
        TokenResponse: JWT токен доступу для автентифікації

    Raises:
        HTTPException:
            - 400: Користувач з таким email вже існує
            - 422: Неправильний формат даних

    Example:
        ```
        POST /auth/signup
        {
            "email": "user@example.com",
            "password": "MySecurePassword123"
        }

        Response:
        {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "token_type": "bearer"
        }
        ```
    """
    try:
        # Створення користувача через сервісний шар
        user = UserService.create_user(db, user_data)

        # Автоматична авторизація після реєстрації
        login_data = UserLogin(email=user.email, password=user_data.password)
        token = UserService.authenticate_user(db, login_data)

        return token

    except HTTPException:
        # Передача HTTP помилок від сервісного шару
        raise
    except Exception as e:
        # Обробка непередбачених помилок
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Помилка сервера при реєстрації: {str(e)}",
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin, db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Авторизація користувача в системі.

    Args:
        login_data (UserLogin): Дані для авторизації (email, password)
        db (Session): Сесія бази даних

    Returns:
        TokenResponse: JWT токен доступу для автентифікації

    Raises:
        HTTPException:
            - 401: Неправильний email або пароль
            - 422: Неправильний формат даних

    Example:
        ```
        POST /auth/login
        {
            "email": "user@example.com",
            "password": "MySecurePassword123"
        }

        Response:
        {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "token_type": "bearer"
        }
        ```
    """
    try:
        # Автентифікація через сервісний шар
        token = UserService.authenticate_user(db, login_data)
        return token

    except HTTPException:
        # Передача HTTP помилок від сервісного шару
        raise
    except Exception as e:
        # Обробка непередбачених помилок
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Помилка сервера при авторизації: {str(e)}",
        )
