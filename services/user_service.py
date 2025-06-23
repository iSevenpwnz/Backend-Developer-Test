"""
Сервісний шар для роботи з користувачами.
Містить бізнес-логіку реєстрації, авторизації та управління користувачами.
"""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from models.user import User
from schemas.user import UserSignup, UserLogin, TokenResponse
from utils.auth import hash_password, verify_password, create_access_token


class UserService:
    """
    Сервіс для управління користувачами.
    Забезпечує бізнес-логіку реєстрації, авторизації та роботи з профілями.
    """

    @staticmethod
    def create_user(db: Session, user_data: UserSignup) -> User:
        """
        Створює нового користувача в системі.

        Args:
            db (Session): Сесія бази даних
            user_data (UserSignup): Дані для реєстрації користувача

        Returns:
            User: Створений користувач

        Raises:
            HTTPException: Якщо користувач з таким email вже існує

        Example:
            >>> user_data = UserSignup(email="test@example.com", password="Password123")
            >>> user = UserService.create_user(db, user_data)
            >>> print(user.email)
            test@example.com
        """
        # Перевірка чи не існує користувач з таким email
        existing_user = (
            db.query(User).filter(User.email == user_data.email).first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Користувач з таким email вже існує",
            )

        # Хешування пароля
        hashed_password = hash_password(user_data.password)

        # Створення нового користувача
        new_user = User(email=user_data.email, hashed_password=hashed_password)

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Помилка створення користувача: користувач з таким email вже існує",
            )

    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> TokenResponse:
        """
        Автентифікує користувача та повертає JWT токен.

        Args:
            db (Session): Сесія бази даних
            login_data (UserLogin): Дані для авторизації

        Returns:
            TokenResponse: JWT токен доступу

        Raises:
            HTTPException: Якщо email або пароль неправильні

        Example:
            >>> login_data = UserLogin(email="test@example.com", password="Password123")
            >>> token = UserService.authenticate_user(db, login_data)
            >>> print(token.access_token)
            eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
        """
        # Пошук користувача за email
        user = db.query(User).filter(User.email == login_data.email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неправильний email або пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Перевірка пароля
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неправильний email або пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Створення JWT токена
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}
        )

        return TokenResponse(access_token=access_token, token_type="bearer")

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Отримує користувача за його ID.

        Args:
            db (Session): Сесія бази даних
            user_id (int): ID користувача

        Returns:
            Optional[User]: Користувач або None якщо не знайдено

        Example:
            >>> user = UserService.get_user_by_id(db, 1)
            >>> if user:
            ...     print(user.email)
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Отримує користувача за його email.

        Args:
            db (Session): Сесія бази даних
            email (str): Email користувача

        Returns:
            Optional[User]: Користувач або None якщо не знайдено

        Example:
            >>> user = UserService.get_user_by_email(db, "test@example.com")
            >>> if user:
            ...     print(user.id)
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def check_user_exists(db: Session, user_id: int) -> bool:
        """
        Перевіряє чи існує користувач з заданим ID.

        Args:
            db (Session): Сесія бази даних
            user_id (int): ID користувача для перевірки

        Returns:
            bool: True якщо користувач існує, False інакше

        Example:
            >>> exists = UserService.check_user_exists(db, 1)
            >>> print(f"Користувач існує: {exists}")
        """
        user = db.query(User).filter(User.id == user_id).first()
        return user is not None
