"""
SEVDO Backend API Schemas
All Pydantic models for API responses and data validation
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# ============================================================================
# AUTH SCHEMAS
# ============================================================================


class User(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    created_at: datetime
    is_active: bool


# ============================================================================
# CONTACT SCHEMAS
# ============================================================================


class ContactFormData(BaseModel):
    name: str
    email: str
    subject: Optional[str] = None
    message: str


# ============================================================================
# BLOG SCHEMAS
# ============================================================================


class BlogPostResponse(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: Optional[str] = None
    featured_image: Optional[str] = None
    published: bool
    created_at: datetime
    updated_at: datetime
    author_id: int
    author_username: Optional[str] = None
    tags: List[str] = []


class BlogTagResponse(BaseModel):
    id: int
    name: str
    post_count: int
    slug: str


class BlogPostsListResponse(BaseModel):
    posts: List[BlogPostResponse]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool


class BlogTagsListResponse(BaseModel):
    tags: List[BlogTagResponse]
    total: int


class TaggedPostsResponse(BaseModel):
    tag: BlogTagResponse
    posts: List[BlogPostResponse]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool


class BlogPostDetailResponse(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: str
    featured_image: Optional[str] = None
    published: bool
    created_at: datetime
    updated_at: datetime
    author_id: int
    author_username: str
    author_email: Optional[str] = None
    tags: List[str] = []
    word_count: int
    reading_time_minutes: int


class BlogSearchResult(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: Optional[str] = None
    featured_image: Optional[str] = None
    created_at: datetime
    author_username: str
    tags: List[str] = []
    match_score: float
    match_type: str  # "title", "content", "tag", "author"


class BlogSearchResponse(BaseModel):
    results: List[BlogSearchResult]
    total: int
    query: str
    page: int
    limit: int
    has_next: bool
    has_prev: bool
    search_time_ms: float
    suggestions: List[str] = []


# ============================================================================
# CHAT SCHEMAS
# ============================================================================


class ChatMessageData(BaseModel):
    message: str
    chat_room: Optional[str] = "general"
    message_type: Optional[str] = "text"  # text, image, file
    reply_to: Optional[int] = None  # ID of message being replied to


# ============================================================================
# EMAIL SCHEMAS
# ============================================================================


class EmailFormData(BaseModel):
    to: str
    subject: str
    message: str
    from_name: Optional[str] = None
