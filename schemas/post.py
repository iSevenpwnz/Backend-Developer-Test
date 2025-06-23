"""
Pydantic схеми для посту з розширеною валідацією полів.
Включає валідацію розміру тексту до 1MB та схеми для всіх операцій з постами.
"""

import sys
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class PostCreate(BaseModel):
    """
    Схема для створення нового посту.

    Attributes:
        text (str): Текст посту (максимум 1MB)
    """

    text: str = Field(
        ...,
        min_length=1,
        description="Текст посту (максимум 1MB)",
        example="Це мій перший пост у додатку!",
    )

    @field_validator("text")
    @classmethod
    def validate_text_size(cls, v):
        """
        Валідація розміру тексту посту (максимум 1MB).

        Args:
            v (str): Текст посту для валідації

        Returns:
            str: Валідний текст посту

        Raises:
            ValueError: Якщо розмір тексту перевищує 1MB
        """
        # Розрахунок розміру в байтах
        text_size = sys.getsizeof(v.encode("utf-8"))
        max_size = 1024 * 1024  # 1MB в байтах

        if text_size > max_size:
            raise ValueError(
                f"Розмір тексту посту не може перевищувати 1MB. Поточний розмір: {text_size} байт"
            )

        return v


class PostUpdate(BaseModel):
    """
    Схема для оновлення існуючого посту.

    Attributes:
        text (str): Новий текст посту (максимум 1MB, опціонально)
    """

    text: Optional[str] = Field(
        None,
        min_length=1,
        description="Новий текст посту (максимум 1MB)",
        example="Оновлений текст мого посту",
    )

    @field_validator("text")
    @classmethod
    def validate_text_size(cls, v):
        """
        Валідація розміру тексту посту (максимум 1MB).

        Args:
            v (str): Текст посту для валідації

        Returns:
            str: Валідний текст посту

        Raises:
            ValueError: Якщо розмір тексту перевищує 1MB
        """
        if v is None:
            return v

        # Розрахунок розміру в байтах
        text_size = sys.getsizeof(v.encode("utf-8"))
        max_size = 1024 * 1024  # 1MB в байтах

        if text_size > max_size:
            raise ValueError(
                f"Розмір тексту посту не може перевищувати 1MB. Поточний розмір: {text_size} байт"
            )

        return v


class PostResponse(BaseModel):
    """
    Схема відповіді з інформацією про пост.

    Attributes:
        id (int): Унікальний ідентифікатор посту
        text (str): Текст посту
        user_id (int): ID користувача-автора
        created_at (datetime): Дата створення посту
        updated_at (datetime): Дата останнього оновлення
    """

    id: int = Field(
        ..., gt=0, description="Унікальний ідентифікатор посту", example=1
    )

    text: str = Field(
        ..., description="Текст посту", example="Це мій перший пост у додатку!"
    )

    user_id: int = Field(
        ..., gt=0, description="ID користувача-автора", example=1
    )

    created_at: datetime = Field(
        ...,
        description="Дата та час створення посту",
        example="2023-01-01T12:00:00Z",
    )

    updated_at: datetime = Field(
        ...,
        description="Дата та час останнього оновлення",
        example="2023-01-01T12:00:00Z",
    )

    class Config:
        """Конфігурація Pydantic моделі"""

        from_attributes = True


class PostDeleteResponse(BaseModel):
    """
    Схема відповіді при видаленні посту.

    Attributes:
        message (str): Повідомлення про успішне видалення
        post_id (int): ID видаленого посту
    """

    message: str = Field(
        ...,
        description="Повідомлення про результат операції",
        example="Пост успішно видалено",
    )

    post_id: int = Field(
        ..., gt=0, description="ID видаленого посту", example=1
    )
