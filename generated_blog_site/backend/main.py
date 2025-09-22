
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship
from typing import Generator, Optional, List, Dict
from datetime import datetime, timedelta
import uuid
import os
from dotenv import load_dotenv
import logging

# Import models and schemas (CORRECTED ORDER)
from models import Base, UserDB, SessionDB, ContactFormDB, BlogPostDB, BlogTagDB, PostTagDB
from schemas import User, UserResponse, ContactFormData, BlogPostResponse, BlogPostsListResponse, BlogTagResponse

# FastAPI app
app = FastAPI(default_response_class=ORJSONResponse)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables from a .env file if present
load_dotenv()
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "app_db")

# uncomment this for postgresql
# DATABASE_URL = (
#     f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# )

DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- Authentication helpers ---- 
TOKEN_HEADER = "Authorization"

def extract_token(auth_header: Optional[str]) -> str:
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    if len(parts) == 1:
        return parts[0]
    raise HTTPException(status_code=401, detail="Invalid Authorization header")

def get_current_session(authorization: Optional[str] = Header(None, alias=TOKEN_HEADER),
                        db: Session = Depends(get_db)) -> "SessionDB":
    token = extract_token(authorization)
    session = db.query(SessionDB).filter(SessionDB.id == token).first()
    if not session or session.expiry < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    return session

def get_current_user(session: "SessionDB" = Depends(get_current_session),
                     db: Session = Depends(get_db)) -> "UserDB":
    user = db.query(UserDB).filter(UserDB.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# Auto-create tables on startup
Base.metadata.create_all(bind=engine)

# Single blog post response model
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

@app.get("/api/blog/posts/{post_id}")
def blog_get_endpoint(
    post_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve specific blog post by ID or slug.
    
    Args:
        post_id: Blog post ID (integer) or slug (string)
    
    Returns:
        BlogPostDetailResponse: Complete blog post with metadata
    """
    # Try first with ID (if numeric)
    post = None
    
    # Check if post_id is numeric (ID) or string (slug)
    if post_id.isdigit():
        # Search by ID
        post_id_int = int(post_id)
        post = db.query(BlogPostDB).filter(BlogPostDB.id == post_id_int).first()
    else:
        # Search by slug
        post = db.query(BlogPostDB).filter(BlogPostDB.slug == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Check if post is published (unless user is author)
    if not post.published:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Get author information
    author = db.query(UserDB).filter(UserDB.id == post.author_id).first()
    if not author:
        raise HTTPException(status_code=500, detail="Author not found")
    
    # Get tags for this post
    tag_query = db.query(BlogTagDB.name).join(
        PostTagDB, BlogTagDB.id == PostTagDB.tag_id
    ).filter(PostTagDB.post_id == post.id)
    
    tags = [tag[0] for tag in tag_query.all()]
    
    # Calculate reading metrics
    word_count = len(post.content.split()) if post.content else 0
    # Assume average reading speed of 200 words per minute
    reading_time_minutes = max(1, round(word_count / 200))
    
    # Build response
    return BlogPostDetailResponse(
        id=post.id,
        title=post.title,
        slug=post.slug,
        excerpt=post.excerpt,
        content=post.content,
        featured_image=post.featured_image,
        published=post.published,
        created_at=post.created_at,
        updated_at=post.updated_at,
        author_id=post.author_id,
        author_username=author.username,
        author_email=author.email,
        tags=tags,
        word_count=word_count,
        reading_time_minutes=reading_time_minutes
    )

# Alternative endpoint for slug-based access
@app.get("/api/blog/slug/{slug}")
def blog_get_by_slug_endpoint(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve blog post by slug (SEO-friendly URL).
    
    Args:
        slug: Blog post slug (URL-friendly identifier)
    
    Returns:
        BlogPostDetailResponse: Complete blog post
    """
    post = db.query(BlogPostDB).filter(BlogPostDB.slug == slug).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    if not post.published:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Get author information
    author = db.query(UserDB).filter(UserDB.id == post.author_id).first()
    if not author:
        raise HTTPException(status_code=500, detail="Author not found")
    
    # Get tags
    tag_query = db.query(BlogTagDB.name).join(
        PostTagDB, BlogTagDB.id == PostTagDB.tag_id
    ).filter(PostTagDB.post_id == post.id)
    
    tags = [tag[0] for tag in tag_query.all()]
    
    # Calculate metrics
    word_count = len(post.content.split()) if post.content else 0
    reading_time_minutes = max(1, round(word_count / 200))
    
    return BlogPostDetailResponse(
        id=post.id,
        title=post.title,
        slug=post.slug,
        excerpt=post.excerpt,
        content=post.content,
        featured_image=post.featured_image,
        published=post.published,
        created_at=post.created_at,
        updated_at=post.updated_at,
        author_id=post.author_id,
        author_username=author.username,
        author_email=author.email,
        tags=tags,
        word_count=word_count,
        reading_time_minutes=reading_time_minutes
    )

# Search result response model
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

@app.get("/api/blog/search")
def blog_search_endpoint(
    q: str,
    page: int = 1,
    limit: int = 10,
    author: Optional[str] = None,
    tag: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    sort: str = "relevance",
    db: Session = Depends(get_db)
):
    """
    Advanced search in blog posts.
    
    Query parameters:
    - q: Search term (required)
    - page: Page number (default: 1)
    - limit: Results per page (default: 10, max: 50)
    - author: Filter by author username
    - tag: Filter by tag
    - date_from: Filter from date (YYYY-MM-DD)
    - date_to: Filter to date (YYYY-MM-DD)
    - sort: Sort order (relevance, date_desc, date_asc, title_asc)
    """
    import time
    start_time = time.time()
    
    # Validation
    if not q or len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")
    
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")
    if limit < 1 or limit > 50:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 50")
    
    query_term = q.strip().lower()
    
    # Base query - only published posts
    base_query = db.query(BlogPostDB).filter(BlogPostDB.published == True)
    
    # Join with author for filtering and result data
    base_query = base_query.join(UserDB, BlogPostDB.author_id == UserDB.id)
    
    # Author filter
    if author:
        base_query = base_query.filter(UserDB.username.ilike(f"%{author}%"))
    
    # Date filters
    if date_from:
        try:
            from_date = datetime.strptime(date_from, "%Y-%m-%d")
            base_query = base_query.filter(BlogPostDB.created_at >= from_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_from format. Use YYYY-MM-DD")
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, "%Y-%m-%d")
            # Add 1 day to include the entire day
            to_date = to_date.replace(hour=23, minute=59, second=59)
            base_query = base_query.filter(BlogPostDB.created_at <= to_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_to format. Use YYYY-MM-DD")
    
    # Tag filter
    if tag:
        base_query = base_query.join(PostTagDB, BlogPostDB.id == PostTagDB.post_id)
        base_query = base_query.join(BlogTagDB, PostTagDB.tag_id == BlogTagDB.id)
        base_query = base_query.filter(BlogTagDB.name.ilike(f"%{tag}%"))
    
    # Text search with scoring
    search_conditions = []
    
    # Title search (highest score)
    title_condition = BlogPostDB.title.ilike(f"%{query_term}%")
    search_conditions.append(title_condition)
    
    # Content search
    content_condition = BlogPostDB.content.ilike(f"%{query_term}%")
    search_conditions.append(content_condition)
    
    # Excerpt search
    excerpt_condition = BlogPostDB.excerpt.ilike(f"%{query_term}%")
    search_conditions.append(excerpt_condition)
    
    # Apply search conditions
    if search_conditions:
        from sqlalchemy import or_
        search_query = base_query.filter(or_(*search_conditions))
    else:
        search_query = base_query
    
    # Get total count
    total = search_query.count()
    
    # Apply sorting
    if sort == "date_asc":
        search_query = search_query.order_by(BlogPostDB.created_at.asc())
    elif sort == "title_asc":
        search_query = search_query.order_by(BlogPostDB.title.asc())
    elif sort == "date_desc":
        search_query = search_query.order_by(BlogPostDB.created_at.desc())
    else:  # relevance (default)
        # Simple relevance: title matches first, then by date
        search_query = search_query.order_by(
            BlogPostDB.title.ilike(f"%{query_term}%").desc(),
            BlogPostDB.created_at.desc()
        )
    
    # Pagination
    offset = (page - 1) * limit
    posts = search_query.offset(offset).limit(limit).all()
    
    # Prepare results with scoring
    results = []
    post_ids = [post.id for post in posts]
    
    # Get tags for all posts
    if post_ids:
        tag_query = db.query(PostTagDB.post_id, BlogTagDB.name).join(
            BlogTagDB, PostTagDB.tag_id == BlogTagDB.id
        ).filter(PostTagDB.post_id.in_(post_ids))
        
        post_tags = {}
        for post_id, tag_name in tag_query:
            if post_id not in post_tags:
                post_tags[post_id] = []
            post_tags[post_id].append(tag_name)
    else:
        post_tags = {}
    
    # Calculate match scores and types
    for post in posts:
        # Simple scoring algorithm
        score = 0.0
        match_type = "content"
        
        title_lower = post.title.lower()
        content_lower = (post.content or "").lower()
        excerpt_lower = (post.excerpt or "").lower()
        
        # Title match (highest score)
        if query_term in title_lower:
            if title_lower == query_term:
                score = 1.0  # Exact title match
            elif title_lower.startswith(query_term):
                score = 0.9  # Title starts with query
            else:
                score = 0.8  # Title contains query
            match_type = "title"
        
        # Excerpt match
        elif query_term in excerpt_lower:
            score = 0.6
            match_type = "excerpt"
        
        # Content match
        elif query_term in content_lower:
            # Count occurrences for better scoring
            occurrences = content_lower.count(query_term)
            score = min(0.5 + (occurrences * 0.05), 0.7)
            match_type = "content"
        
        # Tag match
        post_tag_names = [tag.lower() for tag in post_tags.get(post.id, [])]
        if any(query_term in tag for tag in post_tag_names):
            score = max(score, 0.4)
            if score == 0.4:
                match_type = "tag"
        
        # Get author info
        author = db.query(UserDB).filter(UserDB.id == post.author_id).first()
        
        result = BlogSearchResult(
            id=post.id,
            title=post.title,
            slug=post.slug,
            excerpt=post.excerpt,
            featured_image=post.featured_image,
            created_at=post.created_at,
            author_username=author.username if author else "Unknown",
            tags=post_tags.get(post.id, []),
            match_score=score,
            match_type=match_type
        )
        results.append(result)
    
    # Sort by score if relevance sorting
    if sort == "relevance":
        results.sort(key=lambda x: x.match_score, reverse=True)
    
    # Calculate search time
    search_time_ms = (time.time() - start_time) * 1000
    
    # Generate search suggestions (simple implementation)
    suggestions = []
    if total == 0:
        # Suggest similar terms or popular tags
        popular_tags = db.query(BlogTagDB.name).limit(5).all()
        suggestions = [tag[0] for tag in popular_tags]
    
    # Pagination info
    has_next = offset + limit < total
    has_prev = page > 1
    
    return BlogSearchResponse(
        results=results,
        total=total,
        query=q,
        page=page,
        limit=limit,
        has_next=has_next,
        has_prev=has_prev,
        search_time_ms=round(search_time_ms, 2),
        suggestions=suggestions
    )

# Quick search endpoint for autocomplete
@app.get("/api/blog/search/suggestions")
def blog_search_suggestions_endpoint(
    q: str,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """
    Quick search suggestions for autocomplete.
    
    Args:
        q: Partial search term
        limit: Number of suggestions (max 10)
    
    Returns:
        List of title suggestions
    """
    if len(q.strip()) < 2:
        return {"suggestions": []}
    
    if limit > 10:
        limit = 10
    
    query_term = q.strip()
    
    # Search in titles for quick suggestions
    suggestions = db.query(BlogPostDB.title).filter(
        BlogPostDB.published == True,
        BlogPostDB.title.ilike(f"%{query_term}%")
    ).limit(limit).all()
    
    return {
        "suggestions": [title[0] for title in suggestions]
    }

# Tag response models
class BlogTagResponse(BaseModel):
    id: int
    name: str
    post_count: int
    slug: str

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

@app.get("/api/blog/tags")
def blog_tags_endpoint(
    sort: str = "post_count_desc",
    limit: Optional[int] = None,
    min_posts: int = 1,
    db: Session = Depends(get_db)
):
    """
    List all available blog tags with post counts.
    
    Query parameters:
    - sort: Sort order (post_count_desc, post_count_asc, name_asc, name_desc)
    - limit: Limit number of tags (optional)
    - min_posts: Minimum number of posts to include tag (default: 1)
    """
    # Build query with post counts
    # Count only published posts
    from sqlalchemy import func
    
    tag_query = db.query(
        BlogTagDB.id,
        BlogTagDB.name,
        func.count(PostTagDB.post_id).label('post_count')
    ).outerjoin(
        PostTagDB, BlogTagDB.id == PostTagDB.tag_id
    ).outerjoin(
        BlogPostDB, PostTagDB.post_id == BlogPostDB.id
    ).filter(
        # Only count published posts or tags with no posts
        db.or_(
            BlogPostDB.published == True,
            BlogPostDB.id.is_(None)
        )
    ).group_by(
        BlogTagDB.id, BlogTagDB.name
    ).having(
        func.count(PostTagDB.post_id) >= min_posts
    )
    
    # Apply sorting
    if sort == "post_count_asc":
        tag_query = tag_query.order_by(func.count(PostTagDB.post_id).asc())
    elif sort == "name_asc":
        tag_query = tag_query.order_by(BlogTagDB.name.asc())
    elif sort == "name_desc":
        tag_query = tag_query.order_by(BlogTagDB.name.desc())
    else:  # post_count_desc (default)
        tag_query = tag_query.order_by(func.count(PostTagDB.post_id).desc())
    
    # Apply limit if specified
    if limit and limit > 0:
        tag_query = tag_query.limit(limit)
    
    # Execute query
    tag_results = tag_query.all()
    
    # Build response
    tags = []
    for tag_id, tag_name, post_count in tag_results:
        # Generate slug from tag name
        slug = tag_name.lower().replace(' ', '-').replace('_', '-')
        # Remove special characters for clean URLs
        import re
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        
        tags.append(BlogTagResponse(
            id=tag_id,
            name=tag_name,
            post_count=post_count,
            slug=slug
        ))
    
    return BlogTagsListResponse(
        tags=tags,
        total=len(tags)
    )

@app.get("/api/blog/tags/{tag_name}/posts")
def blog_tag_posts_endpoint(
    tag_name: str,
    page: int = 1,
    limit: int = 10,
    sort: str = "created_at_desc",
    db: Session = Depends(get_db)
):
    """
    Get all posts for a specific tag.
    
    Args:
        tag_name: Tag name or slug
        page: Page number (default: 1)
        limit: Posts per page (default: 10, max: 50)
        sort: Sort order (created_at_desc, created_at_asc, title_asc)
    """
    # Validation
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")
    if limit < 1 or limit > 50:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 50")
    
    # Find tag by name (case insensitive)
    tag = db.query(BlogTagDB).filter(BlogTagDB.name.ilike(tag_name)).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # Build query for posts with this tag
    posts_query = db.query(BlogPostDB).join(
        PostTagDB, BlogPostDB.id == PostTagDB.post_id
    ).filter(
        PostTagDB.tag_id == tag.id,
        BlogPostDB.published == True
    )
    
    # Apply sorting
    if sort == "created_at_asc":
        posts_query = posts_query.order_by(BlogPostDB.created_at.asc())
    elif sort == "title_asc":
        posts_query = posts_query.order_by(BlogPostDB.title.asc())
    else:  # created_at_desc (default)
        posts_query = posts_query.order_by(BlogPostDB.created_at.desc())
    
    # Get total count
    total = posts_query.count()
    
    # Apply pagination
    offset = (page - 1) * limit
    posts = posts_query.offset(offset).limit(limit).all()
    
    # Get post IDs for tag and author queries
    post_ids = [post.id for post in posts]
    
    # Get all tags for these posts
    if post_ids:
        all_tags_query = db.query(PostTagDB.post_id, BlogTagDB.name).join(
            BlogTagDB, PostTagDB.tag_id == BlogTagDB.id
        ).filter(PostTagDB.post_id.in_(post_ids))
        
        post_tags = {}
        for post_id, tag_name in all_tags_query:
            if post_id not in post_tags:
                post_tags[post_id] = []
            post_tags[post_id].append(tag_name)
    else:
        post_tags = {}
    
    # Build post responses
    post_responses = []
    for post in posts:
        # Get author info
        author = db.query(UserDB).filter(UserDB.id == post.author_id).first()
        
        post_data = BlogPostResponse(
            id=post.id,
            title=post.title,
            slug=post.slug,
            excerpt=post.excerpt,
            content=None,  # Don't include full content in list
            featured_image=post.featured_image,
            published=post.published,
            created_at=post.created_at,
            updated_at=post.updated_at,
            author_id=post.author_id,
            author_username=author.username if author else None,
            tags=post_tags.get(post.id, [])
        )
        post_responses.append(post_data)
    
    # Count total posts for this tag
    tag_post_count = db.query(PostTagDB).join(
        BlogPostDB, PostTagDB.post_id == BlogPostDB.id
    ).filter(
        PostTagDB.tag_id == tag.id,
        BlogPostDB.published == True
    ).count()
    
    # Generate tag slug
    tag_slug = tag.name.lower().replace(' ', '-').replace('_', '-')
    import re
    tag_slug = re.sub(r'[^a-z0-9-]', '', tag_slug)
    
    tag_response = BlogTagResponse(
        id=tag.id,
        name=tag.name,
        post_count=tag_post_count,
        slug=tag_slug
    )
    
    # Pagination info
    has_next = offset + limit < total
    has_prev = page > 1
    
    return TaggedPostsResponse(
        tag=tag_response,
        posts=post_responses,
        total=total,
        page=page,
        limit=limit,
        has_next=has_next,
        has_prev=has_prev
    )

@app.get("/api/blog/tags/popular")
def blog_popular_tags_endpoint(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get the most popular tags (most used).
    
    Args:
        limit: Number of tags to return (max 20)
    """
    if limit > 20:
        limit = 20
    
    # Get most used tags
    from sqlalchemy import func
    
    popular_tags = db.query(
        BlogTagDB.id,
        BlogTagDB.name,
        func.count(PostTagDB.post_id).label('post_count')
    ).join(
        PostTagDB, BlogTagDB.id == PostTagDB.tag_id
    ).join(
        BlogPostDB, PostTagDB.post_id == BlogPostDB.id
    ).filter(
        BlogPostDB.published == True
    ).group_by(
        BlogTagDB.id, BlogTagDB.name
    ).order_by(
        func.count(PostTagDB.post_id).desc()
    ).limit(limit).all()
    
    # Build response
    tags = []
    for tag_id, tag_name, post_count in popular_tags:
        slug = tag_name.lower().replace(' ', '-').replace('_', '-')
        import re
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        
        tags.append(BlogTagResponse(
            id=tag_id,
            name=tag_name,
            post_count=post_count,
            slug=slug
        ))
    
    return {
        "tags": tags,
        "total": len(tags)
    }

@app.get("/api/me", response_model=UserResponse)
def me_endpoint(current_user: UserDB = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Requires valid session token in Authorization header.
    """
    return current_user

# Blog post data models
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

class BlogPostsListResponse(BaseModel):
    posts: List[BlogPostResponse]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool


@app.get("/api/blog/posts")
def blog_posts_endpoint(
    page: int = 1,
    limit: int = 10,
    published: Optional[bool] = None,
    author_id: Optional[int] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    sort: str = "created_at_desc",
    include_content: bool = False,
    db: Session = Depends(get_db)
):
    """
    List blog posts with pagination and filtering.
    
    Query parameters:
    - page: Page number (default: 1)
    - limit: Posts per page (default: 10, max: 100)
    - published: Filter by published status (true/false)
    - author_id: Filter by author ID
    - tag: Filter by tag name
    - search: Text search in title and content
    - sort: Sort order (created_at_desc, created_at_asc, title_asc, title_desc)
    - include_content: Include full content (default: false)
    """
    # Validate parameters
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    
    # Base query
    query = db.query(BlogPostDB)
    
    # Join with users for author info
    query = query.join(UserDB, BlogPostDB.author_id == UserDB.id)
    
    # Filter by published status
    if published is not None:
        query = query.filter(BlogPostDB.published == published)
    
    # Filter by author
    if author_id:
        query = query.filter(BlogPostDB.author_id == author_id)
    
    # Filter by tag
    if tag:
        query = query.join(PostTagDB, BlogPostDB.id == PostTagDB.post_id)
        query = query.join(BlogTagDB, PostTagDB.tag_id == BlogTagDB.id)
        query = query.filter(BlogTagDB.name == tag)
    
    # Text search
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                BlogPostDB.title.ilike(search_term),
                BlogPostDB.content.ilike(search_term),
                BlogPostDB.excerpt.ilike(search_term)
            )
        )
    
    # Sorting
    if sort == "created_at_asc":
        query = query.order_by(BlogPostDB.created_at.asc())
    elif sort == "title_asc":
        query = query.order_by(BlogPostDB.title.asc())
    elif sort == "title_desc":
        query = query.order_by(BlogPostDB.title.desc())
    else:  # default: created_at_desc
        query = query.order_by(BlogPostDB.created_at.desc())
    
    # Count total
    total = query.count()
    
    # Pagination
    offset = (page - 1) * limit
    posts = query.offset(offset).limit(limit).all()
    
    # Get tags for each post
    post_ids = [post.id for post in posts]
    if post_ids:
        tag_query = db.query(PostTagDB.post_id, BlogTagDB.name).join(
            BlogTagDB, PostTagDB.tag_id == BlogTagDB.id
        ).filter(PostTagDB.post_id.in_(post_ids))
        post_tags = {}
        for post_id, tag_name in tag_query:
            if post_id not in post_tags:
                post_tags[post_id] = []
            post_tags[post_id].append(tag_name)
    else:
        post_tags = {}
    
    # Build response
    post_responses = []
    for post in posts:
        # Get author info
        author = db.query(UserDB).filter(UserDB.id == post.author_id).first()
        
        post_data = {
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "excerpt": post.excerpt,
            "content": post.content if include_content else None,
            "featured_image": post.featured_image,
            "published": post.published,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "author_id": post.author_id,
            "author_username": author.username if author else None,
            "tags": post_tags.get(post.id, [])
        }
        post_responses.append(post_data)
    
    # Pagination info
    has_next = offset + limit < total
    has_prev = page > 1
    
    return BlogPostsListResponse(
        posts=post_responses,
        total=total,
        page=page,
        limit=limit,
        has_next=has_next,
        has_prev=has_prev
    )

@app.post("/api/login")
def login_endpoint(user: User, db: Session = Depends(get_db)):
    """
    Authenticate user and create session.
    
    Returns session token on successful login.
    """
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    session_id = str(uuid.uuid4())
    expiry = datetime.utcnow() + timedelta(hours=1)
    db.add(SessionDB(id=session_id, user_id=db_user.id, expiry=expiry))
    db.commit()
    return {"session_token": session_id}

@app.post("/api/contact")
def contact_form_handler(form_data: ContactFormData, db: Session = Depends(get_db)):
    """
    Handle contact form submissions.
    
    Validates input, saves to database, and optionally sends notification email.
    """
    # Basic validation
    if not form_data.name.strip():
        raise HTTPException(status_code=400, detail="Name is required")
    if not form_data.email.strip():
        raise HTTPException(status_code=400, detail="Email is required")
    if not form_data.message.strip():
        raise HTTPException(status_code=400, detail="Message is required")
    
    # Email format validation
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, form_data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Save to database
    db_contact = ContactFormDB(
        name=form_data.name.strip(),
        email=form_data.email.strip().lower(),
        subject=form_data.subject.strip() if form_data.subject else None,
        message=form_data.message.strip()
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    # Log the submission
    logging.info(f"Contact form submitted by {form_data.email} - ID: {db_contact.id}")
    
    return {
        "msg": "Contact form submitted successfully",
        "submission_id": db_contact.id,
        "status": "received"
    }

@app.post("/api/register")
def register_endpoint(user: User, db: Session = Depends(get_db)):
    """
    Create new user account.
    
    Checks if username is available and creates user with hashed password.
    """
    # Check if user already exists
    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed = pwd_context.hash(user.password)
    db_user = UserDB(username=user.username, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User registered successfully", "user_id": db_user.id}

