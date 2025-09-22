"""
SEVDO Backend Database Models
All SQLAlchemy models for database tables
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


# ============================================================================
# AUTH MODELS
# ============================================================================


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class SessionDB(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expiry = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================================================
# CONTACT MODELS
# ============================================================================


class ContactFormDB(Base):
    __tablename__ = "contact_forms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)

    def __repr__(self):
        return f"<ContactForm(id={self.id}, email='{self.email}', subject='{self.subject}')>"


# ============================================================================
# BLOG MODELS
# ============================================================================


class BlogPostDB(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True)
    excerpt = Column(Text)
    content = Column(Text, nullable=False)
    featured_image = Column(String(500))
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = Column(Integer, ForeignKey("users.id"))

    # Relationships can be added later if needed
    # author = relationship("UserDB", back_populates="posts")
    # tags = relationship("BlogTagDB", secondary="post_tags", back_populates="posts")


class BlogTagDB(Base):
    __tablename__ = "blog_tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    # posts = relationship("BlogPostDB", secondary="post_tags", back_populates="tags")


class PostTagDB(Base):
    __tablename__ = "post_tags"

    post_id = Column(Integer, ForeignKey("blog_posts.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("blog_tags.id"), primary_key=True)


# ============================================================================
# CHAT MODELS
# ============================================================================


class ChatRoomDB(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_private = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatMessageDB(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chat_room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    message_type = Column(String, default="text")
    reply_to_id = Column(Integer, ForeignKey("chat_messages.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)


# ============================================================================
# EMAIL MODELS
# ============================================================================


class EmailLogDB(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    to_email = Column(String, nullable=False)
    from_email = Column(String, nullable=True)
    from_name = Column(String, nullable=True)
    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String, default="pending")  # pending, sent, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)


# ============================================================================
# MODEL REGISTRY FOR DYNAMIC LOADING
# ============================================================================

# Export all models for easy importing
__all__ = [
    "Base",
    "UserDB",
    "SessionDB",
    "ContactFormDB",
    "BlogPostDB",
    "BlogTagDB",
    "PostTagDB",
    "ChatRoomDB",
    "ChatMessageDB",
    "EmailLogDB",
]
