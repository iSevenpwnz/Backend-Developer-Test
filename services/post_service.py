"""
Сервісний шар для роботи з постами.
Містить бізнес-логіку створення, отримання, оновлення та видалення постів з кешуванням.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.post import Post
from models.user import User
from schemas.post import PostCreate, PostResponse, PostDeleteResponse
from utils.cache import cache


class PostService:
    """
    Сервіс для управління постами.
    Забезпечує бізнес-логіку CRUD операцій з постами та кешування.
    """

    @staticmethod
    def create_post(
        db: Session, post_data: PostCreate, user_id: int
    ) -> PostResponse:
        """
        Створює новий пост для користувача.

        Args:
            db (Session): Сесія бази даних
            post_data (PostCreate): Дані для створення посту
            user_id (int): ID користувача-автора

        Returns:
            PostResponse: Створений пост

        Raises:
            HTTPException: Якщо користувач не знайдений

        Example:
            >>> post_data = PostCreate(text="Мій новий пост")
            >>> post = PostService.create_post(db, post_data, 1)
            >>> print(post.text)
            Мій новий пост
        """
        # Перевірка існування користувача
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Користувача не знайдено",
            )

        # Створення нового посту
        new_post = Post(text=post_data.text, user_id=user_id)

        try:
            db.add(new_post)
            db.commit()
            db.refresh(new_post)

            # Інвалідація кешу користувача після створення посту
            cache.invalidate_user_posts(user_id)

            return PostResponse.model_validate(new_post)

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Помилка створення посту: {str(e)}",
            )

    @staticmethod
    def get_user_posts(db: Session, user_id: int) -> List[PostResponse]:
        """
        Отримує всі пости користувача з кешуванням.

        Args:
            db (Session): Сесія бази даних
            user_id (int): ID користувача

        Returns:
            List[PostResponse]: Список постів користувача

        Example:
            >>> posts = PostService.get_user_posts(db, 1)
            >>> print(f"Знайдено {len(posts)} постів")
        """
        # Спроба отримати з кешу
        cached_posts = cache.get_user_posts(user_id)
        if cached_posts is not None:
            return [PostResponse(**post) for post in cached_posts]

        # Якщо кеш порожній, запит до бази даних
        posts = (
            db.query(Post)
            .filter(Post.user_id == user_id)
            .order_by(Post.created_at.desc())
            .all()
        )

        # Конвертація в Pydantic моделі
        post_responses = [PostResponse.model_validate(post) for post in posts]

        # Збереження в кеш (конвертуємо в dict для серіалізації)
        posts_dict = [post.model_dump() for post in post_responses]
        cache.set_user_posts(user_id, posts_dict)

        return post_responses

    @staticmethod
    def get_post_by_id(
        db: Session, post_id: int, user_id: int
    ) -> Optional[Post]:
        """
        Отримує конкретний пост користувача за ID.

        Args:
            db (Session): Сесія бази даних
            post_id (int): ID посту
            user_id (int): ID користувача-власника

        Returns:
            Optional[Post]: Пост або None якщо не знайдено

        Example:
            >>> post = PostService.get_post_by_id(db, 1, 1)
            >>> if post:
            ...     print(post.text)
        """
        return (
            db.query(Post)
            .filter(Post.id == post_id, Post.user_id == user_id)
            .first()
        )

    @staticmethod
    def delete_post(
        db: Session, post_id: int, user_id: int
    ) -> PostDeleteResponse:
        """
        Видаляє пост користувача.

        Args:
            db (Session): Сесія бази даних
            post_id (int): ID посту для видалення
            user_id (int): ID користувача-власника

        Returns:
            PostDeleteResponse: Підтвердження видалення

        Raises:
            HTTPException: Якщо пост не знайдений або не належить користувачу

        Example:
            >>> result = PostService.delete_post(db, 1, 1)
            >>> print(result.message)
            Пост успішно видалено
        """
        # Пошук посту
        post = (
            db.query(Post)
            .filter(Post.id == post_id, Post.user_id == user_id)
            .first()
        )

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пост не знайдено або він не належить вам",
            )

        try:
            # Видалення посту
            db.delete(post)
            db.commit()

            # Інвалідація кешу користувача після видалення посту
            cache.invalidate_user_posts(user_id)

            return PostDeleteResponse(
                message="Пост успішно видалено", post_id=post_id
            )

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Помилка видалення посту: {str(e)}",
            )

    @staticmethod
    def get_post_stats(db: Session, user_id: int) -> dict:
        """
        Отримує статистику постів користувача.

        Args:
            db (Session): Сесія бази даних
            user_id (int): ID користувача

        Returns:
            dict: Статистика постів

        Example:
            >>> stats = PostService.get_post_stats(db, 1)
            >>> print(f"Всього постів: {stats['total_posts']}")
        """
        total_posts = db.query(Post).filter(Post.user_id == user_id).count()

        return {
            "user_id": user_id,
            "total_posts": total_posts,
            "cache_info": cache.get_cache_info(),
        }

    @staticmethod
    def check_post_ownership(db: Session, post_id: int, user_id: int) -> bool:
        """
        Перевіряє чи належить пост конкретному користувачу.

        Args:
            db (Session): Сесія бази даних
            post_id (int): ID посту
            user_id (int): ID користувача

        Returns:
            bool: True якщо пост належить користувачу

        Example:
            >>> is_owner = PostService.check_post_ownership(db, 1, 1)
            >>> print(f"Є власником: {is_owner}")
        """
        post = (
            db.query(Post)
            .filter(Post.id == post_id, Post.user_id == user_id)
            .first()
        )
        return post is not None
