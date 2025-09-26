# sevdo_backend/endpoints/admin_blog_posts.py
"""
Admin blog posts endpoint - CRUD operations for managing blog posts.
Requires authentication and admin privileges.
"""


def render_endpoint(args=None, props=None):
    """
    Render admin blog posts CRUD endpoint code.

    Args:
        args: String arguments from DSL (optional parameters)
        props: Dictionary of properties from DSL

    Returns:
        String containing FastAPI endpoint code
    """
    # Default values
    endpoint_path = (
        props.get("path", "/api/admin/blog/posts") if props else "/api/admin/blog/posts"
    )

    # Generate the admin blog posts endpoint code
    endpoint_code = f'''
# Admin blog post schemas
class BlogPostCreateData(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    featured_image: Optional[str] = None
    published: bool = False
    tags: List[str] = []

class BlogPostUpdateData(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    featured_image: Optional[str] = None
    published: Optional[bool] = None
    tags: Optional[List[str]] = None

class AdminBlogPostResponse(BaseModel):
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
    tags: List[str] = []
    word_count: int
    reading_time_minutes: int

class AdminBlogPostsListResponse(BaseModel):
    posts: List[AdminBlogPostResponse]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool

# Helper function to create slug from title
def create_slug(title: str) -> str:
    import re
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9-]', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')

# Helper function to calculate reading time
def calculate_reading_time(content: str) -> int:
    import re
    words = len(re.findall(r'\\w+', content))
    # Average reading speed: 200-250 words per minute
    return max(1, round(words / 225))

# GET /api/admin/blog/posts - List all posts (published and unpublished)
@app.get("{endpoint_path}")
def admin_list_blog_posts(
    page: int = 1,
    limit: int = 20,
    published: Optional[bool] = None,
    author_id: Optional[int] = None,
    search: Optional[str] = None,
    sort: str = "created_desc",
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AdminBlogPostsListResponse:
    """
    List all blog posts for admin interface.
    Supports filtering by published status, author, and search.
    """
    # Validate pagination
    if page < 1:
        page = 1
    if limit < 1 or limit > 100:
        limit = 20
    
    # Build query - no join needed since we'll fetch authors separately
    query = db.query(BlogPostDB)
    
    # Apply filters
    if published is not None:
        query = query.filter(BlogPostDB.published == published)
    
    if author_id is not None:
        query = query.filter(BlogPostDB.author_id == author_id)
    
    if search:
        search_term = f"%{{search}}%"
        query = query.filter(
            BlogPostDB.title.ilike(search_term) | 
            BlogPostDB.content.ilike(search_term) |
            BlogPostDB.excerpt.ilike(search_term)
        )
    
    # Apply sorting
    if sort == "created_desc":
        query = query.order_by(BlogPostDB.created_at.desc())
    elif sort == "created_asc":
        query = query.order_by(BlogPostDB.created_at.asc())
    elif sort == "updated_desc":
        query = query.order_by(BlogPostDB.updated_at.desc())
    elif sort == "title_asc":
        query = query.order_by(BlogPostDB.title.asc())
    elif sort == "published_desc":
        query = query.order_by(BlogPostDB.published.desc(), BlogPostDB.created_at.desc())
    else:
        query = query.order_by(BlogPostDB.created_at.desc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * limit
    posts_db = query.offset(offset).limit(limit).all()
    
    # Get all unique author IDs
    author_ids = list(set(post.author_id for post in posts_db))
    
    # Fetch all authors in one query
    authors = db.query(UserDB).filter(UserDB.id.in_(author_ids)).all()
    authors_dict = {{author.id: author.username for author in authors}}
    
    # Convert to response format
    posts = []
    for post_db in posts_db:
        # Get tags for this post
        tags = [
            tag.name for tag in db.query(BlogTagDB)
            .join(PostTagDB, BlogTagDB.id == PostTagDB.tag_id)
            .filter(PostTagDB.post_id == post_db.id)
            .all()
        ]
        
        # Calculate metrics
        word_count = len(post_db.content.split()) if post_db.content else 0
        reading_time = calculate_reading_time(post_db.content or "")
        
        # Get author username
        author_username = authors_dict.get(post_db.author_id, "Unknown")
        
        posts.append(AdminBlogPostResponse(
            id=post_db.id,
            title=post_db.title,
            slug=post_db.slug,
            excerpt=post_db.excerpt,
            content=post_db.content,
            featured_image=post_db.featured_image,
            published=post_db.published,
            created_at=post_db.created_at,
            updated_at=post_db.updated_at,
            author_id=post_db.author_id,
            author_username=author_username,
            tags=tags,
            word_count=word_count,
            reading_time_minutes=reading_time
        ))
    
    # Calculate pagination info
    has_next = (page * limit) < total
    has_prev = page > 1
    
    return AdminBlogPostsListResponse(
        posts=posts,
        total=total,
        page=page,
        limit=limit,
        has_next=has_next,
        has_prev=has_prev
    )'''

    return endpoint_code.strip()


# Register with token "abp"
ENDPOINT_TOKEN = "abp"
