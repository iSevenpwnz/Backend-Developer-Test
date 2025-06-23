"""
Pydantic схеми для користувача з розширеною валідацією полів.
Включає схеми для реєстрації, авторизації та відповідей API.
"""

import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserSignup(BaseModel):
    """
    Схема для реєстрації нового користувача.

    Attributes:
        email (EmailStr): Валідна email адреса
        password (str): Пароль (мін. 8 символів, має містити літери та цифри)
    """

    email: EmailStr = Field(
        ..., description="Email адреса користувача", example="user@example.com"
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Пароль користувача (мін. 8 символів)",
        example="MySecurePassword123",
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        """
        Валідація пароля на складність.

        Args:
            v (str): Пароль для валідації

        Returns:
            str: Валідний пароль

        Raises:
            ValueError: Якщо пароль не відповідає вимогам
        """
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Пароль повинен містити принаймні одну літеру")
        if not re.search(r"\d", v):
            raise ValueError("Пароль повинен містити принаймні одну цифру")
        if not re.search(r"[A-Z]", v):
            raise ValueError(
                "Пароль повинен містити принаймні одну велику літеру"
            )
        return v


class UserLogin(BaseModel):
    """
    Схема для авторизації користувача.

    Attributes:
        email (EmailStr): Валідна email адреса
        password (str): Пароль користувача
    """

    email: EmailStr = Field(
        ..., description="Email адреса користувача", example="user@example.com"
    )

    password: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Пароль користувача",
        example="MySecurePassword123",
    )


class TokenResponse(BaseModel):
    """
    Схема відповіді з токеном авторизації.

    Attributes:
        access_token (str): JWT токен доступу
        token_type (str): Тип токена (завжди "bearer")
    """

    access_token: str = Field(
        ...,
        description="JWT токен доступу",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    )

    token_type: str = Field(
        default="bearer", description="Тип токена", example="bearer"
    )


class UserResponse(BaseModel):
    """
    Схема відповіді з інформацією про користувача.

    Attributes:
        id (int): Унікальний ідентифікатор користувача
        email (str): Email адреса користувача
        created_at (datetime): Дата створення аккаунту
        posts (List[PostResponse]): Список постів користувача (опціонально)
    """

    id: int = Field(
        ...,
        gt=0,
        description="Унікальний ідентифікатор користувача",
        example=1,
    )

    email: str = Field(
        ..., description="Email адреса користувача", example="user@example.com"
    )

    created_at: datetime = Field(
        ...,
        description="Дата та час створення аккаунту",
        example="2023-01-01T12:00:00Z",
    )

    # posts поле видалено для уникнення circular import

    class Config:
        """Конфігурація Pydantic моделі"""

        from_attributes = True


# Циклічна залежність вирішена видаленням posts поля
