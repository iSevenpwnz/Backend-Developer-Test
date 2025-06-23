"""
Система кешування для оптимізації запитів до бази даних.
Реалізує кешування постів користувача на 5 хвилин.
"""

import json
import time
from typing import Any, Optional, List
from cachetools import TTLCache
from datetime import datetime

# Кеш з TTL (Time To Live) 5 хвилин = 300 секунд
# Максимально 1000 записів в кеші
posts_cache = TTLCache(maxsize=1000, ttl=300)


class CacheManager:
    """
    Менеджер кешування для управління збереженням та отриманням даних з кешу.
    Використовує TTL кеш для автоматичного видалення застарілих записів.
    """

    @staticmethod
    def _make_cache_key(user_id: int, prefix: str = "posts") -> str:
        """
        Створює унікальний ключ для кешування.

        Args:
            user_id (int): ID користувача
            prefix (str): Префікс для типу даних (за замовчуванням "posts")

        Returns:
            str: Унікальний ключ кешування

        Example:
            >>> CacheManager._make_cache_key(123)
            'posts:123'
        """
        return f"{prefix}:{user_id}"

    @staticmethod
    def get_user_posts(user_id: int) -> Optional[List[dict]]:
        """
        Отримує пости користувача з кешу.

        Args:
            user_id (int): ID користувача

        Returns:
            Optional[List[dict]]: Список постів з кешу або None якщо кеш порожній

        Example:
            >>> posts = CacheManager.get_user_posts(123)
            >>> if posts:
            ...     print(f"Знайдено {len(posts)} постів у кеші")
        """
        cache_key = CacheManager._make_cache_key(user_id)
        cached_data = posts_cache.get(cache_key)

        if cached_data:
            print(
                f"[CACHE HIT] Знайдено пости для користувача {user_id} у кеші"
            )
            return cached_data.get("posts")

        print(
            f"[CACHE MISS] Пости для користувача {user_id} не знайдено у кеші"
        )
        return None

    @staticmethod
    def set_user_posts(user_id: int, posts: List[dict]) -> None:
        """
        Зберігає пости користувача в кеш.

        Args:
            user_id (int): ID користувача
            posts (List[dict]): Список постів для збереження

        Example:
            >>> posts_data = [{"id": 1, "text": "Hello", "user_id": 123}]
            >>> CacheManager.set_user_posts(123, posts_data)
        """
        cache_key = CacheManager._make_cache_key(user_id)
        cache_data = {
            "posts": posts,
            "cached_at": datetime.utcnow().isoformat(),
            "user_id": user_id,
        }

        posts_cache[cache_key] = cache_data
        print(
            f"[CACHE SET] Збережено {len(posts)} постів для користувача {user_id} у кеш"
        )

    @staticmethod
    def invalidate_user_posts(user_id: int) -> None:
        """
        Видаляє пости користувача з кешу (для оновлення після створення/видалення посту).

        Args:
            user_id (int): ID користувача

        Example:
            >>> CacheManager.invalidate_user_posts(123)
        """
        cache_key = CacheManager._make_cache_key(user_id)

        if cache_key in posts_cache:
            del posts_cache[cache_key]
            print(
                f"[CACHE INVALIDATE] Видалено кеш постів для користувача {user_id}"
            )
        else:
            print(
                f"[CACHE INVALIDATE] Кеш для користувача {user_id} вже порожній"
            )

    @staticmethod
    def get_cache_info() -> dict:
        """
        Отримує інформацію про стан кешу (для моніторингу).

        Returns:
            dict: Статистика кешу

        Example:
            >>> info = CacheManager.get_cache_info()
            >>> print(f"Записів у кеші: {info['size']}")
        """
        return {
            "size": len(posts_cache),
            "maxsize": posts_cache.maxsize,
            "ttl": posts_cache.ttl,
            "hits": getattr(posts_cache, "hits", 0),
            "misses": getattr(posts_cache, "misses", 0),
            "current_time": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def clear_cache() -> None:
        """
        Очищає весь кеш (для тестування або адміністративних цілей).

        Example:
            >>> CacheManager.clear_cache()
        """
        posts_cache.clear()
        print("[CACHE CLEAR] Кеш повністю очищено")


# Alias для зручності використання
cache = CacheManager()
