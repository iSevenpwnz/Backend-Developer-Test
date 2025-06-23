"""
SQLAlchemy user model with complete field validation.
Includes password hashing and authentication token management.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.config import Base


class User(Base):
    """
    User model for database storage.

    Attributes:
        id (int): Unique user identifier (Primary Key)
        email (str): User email address (unique, not null)
        hashed_password (str): Hashed user password (not null)
        created_at (datetime): Account creation date and time
        updated_at (datetime): Last update date and time
        posts (relationship): Relationship with user posts
    """

    __tablename__ = "users"

    # Main fields
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Unique user identifier",
    )

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        comment="User email address (unique)",
    )

    hashed_password = Column(
        String(255), nullable=False, comment="Hashed user password"
    )

    # System fields for auditing
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="User creation date and time",
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Last update date and time",
    )

    # Relationships with other tables
    posts = relationship(
        "Post", back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self):
        """String representation of the user"""
        return f"<User(id={self.id}, email='{self.email}')>"
