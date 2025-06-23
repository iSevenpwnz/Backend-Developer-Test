"""
Caching system for database query optimization.
Implements user post caching for 5 minutes.
"""

import json
import time
from typing import Any, Optional, List
from cachetools import TTLCache
from datetime import datetime

# TTL (Time To Live) cache 5 minutes = 300 seconds
# Maximum 1000 records in cache
posts_cache = TTLCache(maxsize=1000, ttl=300)


class CacheManager:
    """
    Cache manager for managing data storage and retrieval from cache.
    Uses TTL cache for automatic removal of stale records.
    """

    @staticmethod
    def _make_cache_key(user_id: int, prefix: str = "posts") -> str:
        """
        Creates unique key for caching.

        Args:
            user_id (int): User ID
            prefix (str): Data type prefix (default "posts")

        Returns:
            str: Unique cache key

        Example:
            >>> CacheManager._make_cache_key(123)
            'posts:123'
        """
        return f"{prefix}:{user_id}"

    @staticmethod
    def get_user_posts(user_id: int) -> Optional[List[dict]]:
        """
        Gets user posts from cache.

        Args:
            user_id (int): User ID

        Returns:
            Optional[List[dict]]: List of posts from cache or None if cache empty

        Example:
            >>> posts = CacheManager.get_user_posts(123)
            >>> if posts:
            ...     print(f"Found {len(posts)} posts in cache")
        """
        cache_key = CacheManager._make_cache_key(user_id)
        cached_data = posts_cache.get(cache_key)

        if cached_data:
            print(f"[CACHE HIT] Found posts for user {user_id} in cache")
            return cached_data.get("posts")

        print(f"[CACHE MISS] Posts for user {user_id} not found in cache")
        return None

    @staticmethod
    def set_user_posts(user_id: int, posts: List[dict]) -> None:
        """
        Stores user posts in cache.

        Args:
            user_id (int): User ID
            posts (List[dict]): List of posts to store

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
            f"[CACHE SET] Stored {len(posts)} posts for user {user_id} in cache"
        )

    @staticmethod
    def invalidate_user_posts(user_id: int) -> None:
        """
        Removes user posts from cache (for refresh after create/delete post).

        Args:
            user_id (int): User ID

        Example:
            >>> CacheManager.invalidate_user_posts(123)
        """
        cache_key = CacheManager._make_cache_key(user_id)

        if cache_key in posts_cache:
            del posts_cache[cache_key]
            print(f"[CACHE INVALIDATE] Removed post cache for user {user_id}")
        else:
            print(f"[CACHE INVALIDATE] Cache for user {user_id} already empty")

    @staticmethod
    def get_cache_info() -> dict:
        """
        Gets cache status information (for monitoring).

        Returns:
            dict: Cache statistics

        Example:
            >>> info = CacheManager.get_cache_info()
            >>> print(f"Cache records: {info['size']}")
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
        Clears entire cache (for testing or administrative purposes).

        Example:
            >>> CacheManager.clear_cache()
        """
        posts_cache.clear()
        print("[CACHE CLEAR] Cache completely cleared")


# Alias for convenience
cache = CacheManager()
