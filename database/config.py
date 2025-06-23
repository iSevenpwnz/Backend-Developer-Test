"""
Конфігурація бази даних для підключення до MySQL через SQLAlchemy.
Налаштовує сесії та базову модель для всіх таблиць.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

# URL підключення до бази даних (SQLite для демонстрації, MySQL для продакшену)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fastapi_app.db")

# Створення engine для підключення до бази даних
if DATABASE_URL.startswith("sqlite"):
    # Для SQLite
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Логування SQL запитів для розробки
        connect_args={"check_same_thread": False},
    )
else:
    # Для MySQL та інших БД
    engine = create_engine(
        DATABASE_URL,
        echo=True,  # Логування SQL запитів для розробки
        pool_pre_ping=True,  # Перевірка з'єднання перед використанням
        pool_recycle=3600,  # Оновлення з'єднань кожну годину
    )

# Фабрика сесій для роботи з базою даних
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базова модель для всіх таблиць
Base = declarative_base()


def get_db():
    """
    Генератор сесій бази даних для dependency injection.
    Забезпечує автоматичне закриття сесії після використання.

    Yields:
        Session: Сесія SQLAlchemy для роботи з базою даних
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
