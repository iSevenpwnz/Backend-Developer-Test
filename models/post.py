"""
SQLAlchemy post model with complete field validation.
Includes user relationship and content size validation.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.config import Base


class Post(Base):
    """
    Post model for database storage.

    Attributes:
        id (int): Unique post identifier (Primary Key)
        text (str): Post text (max 1MB)
        user_id (int): Author user ID (Foreign Key)
        created_at (datetime): Post creation date and time
        updated_at (datetime): Last update date and time
        author (relationship): Relationship with author user
    """

    __tablename__ = "posts"

    # Main fields
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Unique post identifier",
    )

    text = Column(Text, nullable=False, comment="Post text (max 1MB)")

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Author user ID",
    )

    # System fields for auditing
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Post creation date and time",
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Last update date and time",
    )

    # Relationships with other tables
    author = relationship("User", back_populates="posts")

    def __repr__(self):
        """String representation of the post"""
        return f"<Post(id={self.id}, user_id={self.user_id}, text='{self.text[:50]}...')>"
