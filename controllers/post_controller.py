"""
Контролер для роботи з постами.
Містить ендпоінти для створення, отримання та видалення постів з автентифікацією.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from schemas.post import PostCreate, PostResponse, PostDeleteResponse
from services.post_service import PostService
from utils.dependencies import get_current_user_id

# Створення роутера для постів
router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=PostResponse, status_code=status.HTTP_201_CREATED
)
async def add_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> PostResponse:
    """
    Створює новий пост для автентифікованого користувача.

    Валідує розмір payload (максимум 1MB) через Pydantic схему.
    Використовує dependency injection для автентифікації токена.

    Args:
        post_data (PostCreate): Дані для створення посту
        db (Session): Сесія бази даних
        current_user_id (int): ID поточного користувача з токена

    Returns:
        PostResponse: Створений пост з усіма деталями

    Raises:
        HTTPException:
            - 401: Недійсний або відсутній токен
            - 422: Неправильний формат даних або розмір > 1MB
            - 404: Користувач не знайдений

    Example:
        ```
        POST /posts/
        Headers: Authorization: Bearer <jwt-token>
        {
            "text": "Це мій новий пост у додатку!"
        }

        Response:
        {
            "id": 1,
            "text": "Це мій новий пост у додатку!",
            "user_id": 1,
            "created_at": "2023-01-01T12:00:00Z",
            "updated_at": "2023-01-01T12:00:00Z"
        }
        ```
    """
    try:
        # Створення посту через сервісний шар
        new_post = PostService.create_post(db, post_data, current_user_id)
        return new_post

    except HTTPException:
        # Передача HTTP помилок від сервісного шару
        raise
    except Exception as e:
        # Обробка непередбачених помилок
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Помилка сервера при створенні посту: {str(e)}",
        )


@router.get("/", response_model=List[PostResponse])
async def get_posts(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> List[PostResponse]:
    """
    Отримує всі пости автентифікованого користувача.

    Використовує кешування на 5 хвилин для оптимізації.
    Dependency injection забезпечує автентифікацію токена.

    Args:
        db (Session): Сесія бази даних
        current_user_id (int): ID поточного користувача з токена

    Returns:
        List[PostResponse]: Список постів користувача (від найновіших)

    Raises:
        HTTPException:
            - 401: Недійсний або відсутній токен

    Example:
        ```
        GET /posts/
        Headers: Authorization: Bearer <jwt-token>

        Response:
        [
            {
                "id": 2,
                "text": "Мій другий пост",
                "user_id": 1,
                "created_at": "2023-01-01T13:00:00Z",
                "updated_at": "2023-01-01T13:00:00Z"
            },
            {
                "id": 1,
                "text": "Мій перший пост",
                "user_id": 1,
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-01T12:00:00Z"
            }
        ]
        ```
    """
    try:
        # Отримання постів через сервісний шар (з кешуванням)
        posts = PostService.get_user_posts(db, current_user_id)
        return posts

    except HTTPException:
        # Передача HTTP помилок від сервісного шару
        raise
    except Exception as e:
        # Обробка непередбачених помилок
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Помилка сервера при отриманні постів: {str(e)}",
        )


@router.delete("/{post_id}", response_model=PostDeleteResponse)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> PostDeleteResponse:
    """
    Видаляє конкретний пост автентифікованого користувача.

    Перевіряє права власності на пост перед видаленням.
    Dependency injection забезпечує автентифікацію токена.

    Args:
        post_id (int): ID посту для видалення
        db (Session): Сесія бази даних
        current_user_id (int): ID поточного користувача з токена

    Returns:
        PostDeleteResponse: Підтвердження видалення з ID посту

    Raises:
        HTTPException:
            - 401: Недійсний або відсутній токен
            - 404: Пост не знайдений або не належить користувачу

    Example:
        ```
        DELETE /posts/1
        Headers: Authorization: Bearer <jwt-token>

        Response:
        {
            "message": "Пост успішно видалено",
            "post_id": 1
        }
        ```
    """
    try:
        # Видалення посту через сервісний шар
        result = PostService.delete_post(db, post_id, current_user_id)
        return result

    except HTTPException:
        # Передача HTTP помилок від сервісного шару
        raise
    except Exception as e:
        # Обробка непередбачених помилок
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Помилка сервера при видаленні посту: {str(e)}",
        )


@router.get("/stats", response_model=dict)
async def get_post_stats(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> dict:
    """
    Отримує статистику постів користувача та інформацію про кеш.

    Додатковий ендпоінт для моніторингу та дебагу.

    Args:
        db (Session): Сесія бази даних
        current_user_id (int): ID поточного користувача з токена

    Returns:
        dict: Статистика постів та кешу

    Example:
        ```
        GET /posts/stats
        Headers: Authorization: Bearer <jwt-token>

        Response:
        {
            "user_id": 1,
            "total_posts": 5,
            "cache_info": {
                "size": 1,
                "maxsize": 1000,
                "ttl": 300
            }
        }
        ```
    """
    try:
        # Отримання статистики через сервісний шар
        stats = PostService.get_post_stats(db, current_user_id)
        return stats

    except Exception as e:
        # Обробка непередбачених помилок
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Помилка сервера при отриманні статистики: {str(e)}",
        )
