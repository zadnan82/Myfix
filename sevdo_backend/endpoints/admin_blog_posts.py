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
    
    # Build query
    query = db.query(BlogPostDB).join(UserDB, BlogPostDB.author_id == UserDB.id)
    
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
            author_username=post_db.author.username,
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
    )

# POST /api/admin/blog/posts - Create new blog post
@app.post("{endpoint_path}")
def admin_create_blog_post(
    post_data: BlogPostCreateData,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AdminBlogPostResponse:
    """
    Create a new blog post.
    """
    # Generate slug from title
    slug = create_slug(post_data.title)
    
    # Ensure slug is unique
    counter = 1
    original_slug = slug
    while db.query(BlogPostDB).filter(BlogPostDB.slug == slug).first():
        slug = f"{{original_slug}}-{{counter}}"
        counter += 1
    
    # Create blog post
    blog_post = BlogPostDB(
        title=post_data.title,
        slug=slug,
        content=post_data.content,
        excerpt=post_data.excerpt,
        featured_image=post_data.featured_image,
        published=post_data.published,
        author_id=current_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(blog_post)
    db.commit()
    db.refresh(blog_post)
    
    # Handle tags
    if post_data.tags:
        for tag_name in post_data.tags:
            # Get or create tag
            tag = db.query(BlogTagDB).filter(BlogTagDB.name == tag_name).first()
            if not tag:
                tag_slug = create_slug(tag_name)
                tag = BlogTagDB(name=tag_name, slug=tag_slug)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            
            # Create post-tag relationship
            post_tag = PostTagDB(post_id=blog_post.id, tag_id=tag.id)
            db.add(post_tag)
        
        db.commit()
    
    # Return created post
    word_count = len(blog_post.content.split()) if blog_post.content else 0
    reading_time = calculate_reading_time(blog_post.content or "")
    
    return AdminBlogPostResponse(
        id=blog_post.id,
        title=blog_post.title,
        slug=blog_post.slug,
        excerpt=blog_post.excerpt,
        content=blog_post.content,
        featured_image=blog_post.featured_image,
        published=blog_post.published,
        created_at=blog_post.created_at,
        updated_at=blog_post.updated_at,
        author_id=blog_post.author_id,
        author_username=current_user.username,
        tags=post_data.tags,
        word_count=word_count,
        reading_time_minutes=reading_time
    )

# GET /api/admin/blog/posts/{{post_id}} - Get specific post for editing
@app.get("{endpoint_path}/{{post_id}}")
def admin_get_blog_post(
    post_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AdminBlogPostResponse:
    """
    Get a specific blog post for editing.
    """
    post_db = db.query(BlogPostDB).filter(BlogPostDB.id == post_id).first()
    if not post_db:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Get tags
    tags = [
        tag.name for tag in db.query(BlogTagDB)
        .join(PostTagDB, BlogTagDB.id == PostTagDB.tag_id)
        .filter(PostTagDB.post_id == post_db.id)
        .all()
    ]
    
    # Get author info
    author = db.query(UserDB).filter(UserDB.id == post_db.author_id).first()
    
    # Calculate metrics
    word_count = len(post_db.content.split()) if post_db.content else 0
    reading_time = calculate_reading_time(post_db.content or "")
    
    return AdminBlogPostResponse(
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
        author_username=author.username if author else "Unknown",
        tags=tags,
        word_count=word_count,
        reading_time_minutes=reading_time
    )

# PUT /api/admin/blog/posts/{{post_id}} - Update existing post
@app.put("{endpoint_path}/{{post_id}}")
def admin_update_blog_post(
    post_id: int,
    post_data: BlogPostUpdateData,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AdminBlogPostResponse:
    """
    Update an existing blog post.
    """
    post_db = db.query(BlogPostDB).filter(BlogPostDB.id == post_id).first()
    if not post_db:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Update fields if provided
    if post_data.title is not None:
        post_db.title = post_data.title
        # Update slug if title changed
        new_slug = create_slug(post_data.title)
        if new_slug != post_db.slug:
            # Ensure new slug is unique
            counter = 1
            original_slug = new_slug
            while db.query(BlogPostDB).filter(
                BlogPostDB.slug == new_slug, 
                BlogPostDB.id != post_id
            ).first():
                new_slug = f"{{original_slug}}-{{counter}}"
                counter += 1
            post_db.slug = new_slug
    
    if post_data.content is not None:
        post_db.content = post_data.content
    
    if post_data.excerpt is not None:
        post_db.excerpt = post_data.excerpt
    
    if post_data.featured_image is not None:
        post_db.featured_image = post_data.featured_image
    
    if post_data.published is not None:
        post_db.published = post_data.published
    
    post_db.updated_at = datetime.utcnow()
    
    # Handle tags if provided
    if post_data.tags is not None:
        # Remove existing tags
        db.query(PostTagDB).filter(PostTagDB.post_id == post_id).delete()
        
        # Add new tags
        for tag_name in post_data.tags:
            # Get or create tag
            tag = db.query(BlogTagDB).filter(BlogTagDB.name == tag_name).first()
            if not tag:
                tag_slug = create_slug(tag_name)
                tag = BlogTagDB(name=tag_name, slug=tag_slug)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            
            # Create post-tag relationship
            post_tag = PostTagDB(post_id=post_id, tag_id=tag.id)
            db.add(post_tag)
    
    db.commit()
    db.refresh(post_db)
    
    # Get updated tags
    tags = [
        tag.name for tag in db.query(BlogTagDB)
        .join(PostTagDB, BlogTagDB.id == PostTagDB.tag_id)
        .filter(PostTagDB.post_id == post_id)
        .all()
    ]
    
    # Get author info
    author = db.query(UserDB).filter(UserDB.id == post_db.author_id).first()
    
    # Calculate metrics
    word_count = len(post_db.content.split()) if post_db.content else 0
    reading_time = calculate_reading_time(post_db.content or "")
    
    return AdminBlogPostResponse(
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
        author_username=author.username if author else "Unknown",
        tags=tags,
        word_count=word_count,
        reading_time_minutes=reading_time
    )

# DELETE /api/admin/blog/posts/{{post_id}} - Delete post
@app.delete("{endpoint_path}/{{post_id}}")
def admin_delete_blog_post(
    post_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a blog post and all associated data.
    """
    post_db = db.query(BlogPostDB).filter(BlogPostDB.id == post_id).first()
    if not post_db:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Remove tag associations
    db.query(PostTagDB).filter(PostTagDB.post_id == post_id).delete()
    
    # Delete the post
    db.delete(post_db)
    db.commit()
    
    return {{"message": "Blog post deleted successfully", "id": post_id}}

# PATCH /api/admin/blog/posts/{{post_id}}/publish - Toggle publish status
@app.patch("{endpoint_path}/{{post_id}}/publish")
def admin_toggle_blog_post_publish(
    post_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle the published status of a blog post.
    """
    post_db = db.query(BlogPostDB).filter(BlogPostDB.id == post_id).first()
    if not post_db:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Toggle published status
    post_db.published = not post_db.published
    post_db.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(post_db)
    
    return {{
        "message": f"Post {{'published' if post_db.published else 'unpublished'}} successfully",
        "id": post_id,
        "published": post_db.published
    }}'''

    return endpoint_code.strip()


# Required models for this endpoint
REQUIRED_MODELS = ["blog_models", "auth_models"]

# Register with token "abp" (admin blog posts)
ENDPOINT_TOKEN = "abp"
