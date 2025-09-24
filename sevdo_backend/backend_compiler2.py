from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
import os
import threading
from time import time
from hashlib import sha256
import concurrent.futures as cf

# Import endpoint registry
from endpoints import (
    load_all_endpoints,
    get_endpoint_module,
    list_available_tokens,
)

# Core imports that are always included
CORE_IMPORTS = """
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
from models import Base, UserDB, SessionDB, ContactFormDB, BlogPostDB, BlogTagDB, PostTagDB, NewsletterSubscriberDB, ChatRoomDB, ChatMessageDB, EmailLogDB
from schemas import User, UserResponse, ContactFormData, BlogPostResponse, BlogPostsListResponse, BlogTagResponse, BlogPostDetailResponse, BlogSearchResult, BlogSearchResponse, BlogTagsListResponse, TaggedPostsResponse, NewsletterSubscriptionData, ChatMessageData, EmailFormData

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

@app.on_event("startup")
def seed_database():
    \"\"\"Create test data if database is empty\"\"\"
    db = SessionLocal()
    try:
        # Only seed if no blog posts exist
        if db.query(BlogPostDB).count() == 0:
            print("🌱 Seeding database with test data...")
            
            # Create test user
            test_user = UserDB(
                username="admin", 
                password=pwd_context.hash("admin123"), 
                email="admin@devinsights.com",
                is_active=True
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            
            # Create test tags first
            tags_data = [
                "React", "Design", "Tutorial", "JavaScript", "Web Development", "TypeScript"
            ]
            
            tag_objects = {}
            for tag_name in tags_data:
                tag = BlogTagDB(name=tag_name)
                db.add(tag)
                tag_objects[tag_name] = tag
            
            db.commit()
            
            # Create test blog posts (using data from blog_list.py)
            posts_data = [
                {
                    "title": "Getting Started with React Hooks",
                    "content": "Learn how to use React Hooks to build more efficient and cleaner functional components in your applications. React Hooks revolutionized how we write React components by allowing us to use state and other React features in functional components. This comprehensive guide will take you through everything you need to know about React Hooks, from the basics to advanced patterns.",
                    "excerpt": "Learn how to use React Hooks to build more efficient and cleaner functional components in your applications.",
                    "slug": "getting-started-with-react-hooks",
                    "tags": ["React", "JavaScript", "Tutorial"],
                },
                {
                    "title": "CSS Grid vs Flexbox: When to Use What",
                    "content": "A comprehensive guide to understanding the differences between CSS Grid and Flexbox and when to use each layout method. Both CSS Grid and Flexbox are powerful layout systems, but they serve different purposes. Understanding when to use each one will make you a more effective web developer.",
                    "excerpt": "A comprehensive guide to understanding the differences between CSS Grid and Flexbox and when to use each layout method.",
                    "slug": "css-grid-vs-flexbox-when-to-use-what",
                    "tags": ["Design", "Web Development"],
                },
                {
                    "title": "Building REST APIs with Node.js",
                    "content": "Step-by-step tutorial on creating robust and scalable REST APIs using Node.js, Express, and MongoDB. REST APIs are the backbone of modern web applications. In this tutorial, we'll build a complete API from scratch, covering authentication, validation, error handling, and best practices.",
                    "excerpt": "Step-by-step tutorial on creating robust and scalable REST APIs using Node.js, Express, and MongoDB.",
                    "slug": "building-rest-apis-with-nodejs",
                    "tags": ["JavaScript", "Tutorial", "Web Development"],
                },
                {
                    "title": "Modern JavaScript ES6+ Features",
                    "content": "Explore the latest JavaScript features including arrow functions, destructuring, async/await, and more. ES6+ brought many powerful features to JavaScript that make code more readable, maintainable, and enjoyable to write. Let's explore these features with practical examples.",
                    "excerpt": "Explore the latest JavaScript features including arrow functions, destructuring, async/await, and more.",
                    "slug": "modern-javascript-es6-plus-features", 
                    "tags": ["JavaScript", "Tutorial"],
                },
                {
                    "title": "Responsive Web Design Best Practices",
                    "content": "Learn the fundamental principles of responsive web design and how to create websites that work on all devices. Responsive design is no longer optional - it's essential. This guide covers everything from flexible grids to media queries and modern CSS techniques.",
                    "excerpt": "Learn the fundamental principles of responsive web design and how to create websites that work on all devices.",
                    "slug": "responsive-web-design-best-practices",
                    "tags": ["Design", "Web Development"],
                },
                {
                    "title": "Introduction to TypeScript",
                    "content": "Discover how TypeScript can improve your JavaScript development with static typing and better tooling. TypeScript adds type safety to JavaScript, making your code more reliable and easier to maintain. Learn the basics and see how it can transform your development workflow.",
                    "excerpt": "Discover how TypeScript can improve your JavaScript development with static typing and better tooling.",
                    "slug": "introduction-to-typescript",
                    "tags": ["TypeScript", "JavaScript", "Tutorial"],
                },
            ]
            
            # Create blog posts
            for i, post_data in enumerate(posts_data):
                post = BlogPostDB(
                    title=post_data["title"],
                    slug=post_data["slug"],
                    content=post_data["content"],
                    excerpt=post_data["excerpt"],
                    published=True,
                    author_id=test_user.id,
                    created_at=datetime.utcnow() - timedelta(days=i*2)  # Spread posts over time
                )
                db.add(post)
                db.commit()
                db.refresh(post)
                
                # Add tags to posts
                for tag_name in post_data["tags"]:
                    if tag_name in tag_objects:
                        post_tag = PostTagDB(post_id=post.id, tag_id=tag_objects[tag_name].id)
                        db.add(post_tag)
                
            db.commit()
            print(f"✅ Seeded database with {len(posts_data)} blog posts and {len(tags_data)} tags")
        else:
            print("ℹ️  Database already contains data, skipping seed")
            
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

"""

# Legacy mapping for backward compatibility
legacy_mapping = {
    "r": """
@app.post("/register")
def register_endpoint(user: User, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed = pwd_context.hash(user.password)
    db_user = UserDB(username=user.username, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User registered successfully", "user_id": db_user.id}""",
    "l": """
@app.post("/login")
def login_endpoint(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    session_id = str(uuid.uuid4())
    expiry = datetime.utcnow() + timedelta(hours=1)
    db.add(SessionDB(id=session_id, user_id=db_user.id, expiry=expiry))
    db.commit()
    return {"session_token": session_id}""",
    "o": """
@app.post("/logout")
def logout_endpoint(session: SessionDB = Depends(get_current_session), db: Session = Depends(get_db)):
    db.delete(session)
    db.commit()
    return {"msg": "Logged out successfully"}""",
    "u": """
@app.post("/update")
def update_endpoint(user: User, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.password = pwd_context.hash(user.password)
    db.commit()
    return {"msg": "Password updated successfully"}""",
    "m": """
@app.get("/me", response_model=UserResponse)
def me_endpoint(current_user: UserDB = Depends(get_current_user)):
    return current_user""",
    "t": """
@app.post("/refresh")
def refresh_endpoint(session: SessionDB = Depends(get_current_session), db: Session = Depends(get_db)):
    new_session_id = str(uuid.uuid4())
    session.id = new_session_id
    session.expiry = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    return {"session_token": new_session_id}""",
    "a": """
@app.post("/logout-all")
def logout_all_endpoint(current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(SessionDB).filter(SessionDB.user_id == current_user.id).delete()
    db.commit()
    return {"msg": "Logged out of all sessions"}""",
    "s": """
@app.get("/sessions")
def list_sessions_endpoint(current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    sessions = db.query(SessionDB).filter(SessionDB.user_id == current_user.id).all()
    return [{"id": s.id, "expiry": s.expiry.isoformat(), "created_at": s.created_at.isoformat()} for s in sessions]""",
    "k": """
@app.delete("/sessions/{session_id}")
def revoke_session_endpoint(session_id: str, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(SessionDB).filter(SessionDB.id == session_id, SessionDB.user_id == current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()
    return {"msg": "Session revoked successfully"}""",
}


class BackendCompiler:
    def __init__(self):
        # Load all endpoint modules
        load_all_endpoints()

        # Combine legacy mapping with dynamic endpoints
        self.mapping = legacy_mapping.copy()

        # Add dynamically loaded endpoints - NEW ENDPOINTS OVERRIDE LEGACY
        available_tokens = list_available_tokens()
        for token in available_tokens:
            module = get_endpoint_module(token)
            if module and hasattr(module, "render_endpoint"):
                # Let new endpoints override legacy
                self.mapping[token] = module

        # Build index of (method, path) -> token for reverse lookup
        self._route_index = self._build_route_index()

    def _get_required_model_modules(self, tokens):
        """Get required model modules based on endpoint specifications"""
        model_modules = set()

        # Always include auth models
        model_modules.add("auth_models")

        # Check each token for required models
        for token in tokens:
            # 1. First check dynamic endpoints (NEW OVERRIDES LEGACY)
            module = get_endpoint_module(token)
            if module and hasattr(module, "REQUIRED_MODELS"):
                required = module.REQUIRED_MODELS
                if isinstance(required, list):
                    model_modules.update(required)
                elif isinstance(required, str):
                    model_modules.add(required)

            # 2. Fallback to legacy only if no dynamic endpoint found
            elif token in {"bp", "bg", "bt", "bs"}:
                model_modules.add("blog_models")

    def _generate_model_imports(self, model_modules):
        """Generate import code for required models - DEPRECATED (now using centralized models.py)"""
        return ""  # No longer needed since we have centralized models.py

    def _build_route_index(self):
        index = {}
        for token, snippet_or_module in self.mapping.items():
            if isinstance(snippet_or_module, str):
                # Legacy string-based mapping
                decorator_start = snippet_or_module.find("@app.")
                if decorator_start == -1:
                    continue
                line_end = snippet_or_module.find("\n", decorator_start)
                line = snippet_or_module[
                    decorator_start : line_end if line_end != -1 else None
                ]
                try:
                    after_app = line.split("@app.", 1)[1]
                    method = after_app.split("(", 1)[0].strip()
                    first_quote = line.find('"', line.find("(") + 1)
                    second_quote = line.find('"', first_quote + 1)
                    path = line[first_quote + 1 : second_quote]
                    index[(method.upper(), path)] = token
                except Exception:
                    continue
            # For module-based endpoints, we'd need to extract path info from the module
            # This could be added later if needed
        return index

    def tokens_to_code(self, tokens, include_imports=True):
        tokens = list(tokens)
        parts = []

        if include_imports:
            # Add core imports (includes all models and schemas now)
            parts.append(CORE_IMPORTS)

        for token in tokens:
            if token in self.mapping:
                item = self.mapping[token]
                if isinstance(item, str):
                    # Legacy string-based endpoint
                    parts.append(item + "\n\n")
                else:
                    # Module-based endpoint
                    try:
                        code = item.render_endpoint()
                        parts.append(code + "\n\n")
                    except Exception as e:
                        print(f"Error rendering endpoint {token}: {e}")
                        continue

        return "".join(parts)

    def file_tokens_to_code(self, input_path="input.txt", output_path="output.py"):
        with open(input_path, "r") as f:
            tokens = f.read().split()
        code = self.tokens_to_code(tokens)
        with open(output_path, "w") as f:
            f.write(code)
        return code

    def code_to_tokens(self, code):
        found = []  # list of (pos, token)
        for (method, path), token in self._route_index.items():
            signature = f'@app.{method.lower()}("{path}")'
            pos = code.find(signature)
            if pos != -1:
                found.append((pos, token))
        found.sort(key=lambda x: x[0])
        return [t for _, t in found]

    def file_code_to_tokens(self, code_path="output.py"):
        with open(code_path, "r") as f:
            code = f.read()
        return self.code_to_tokens(code)

    def list_available_endpoints(self):
        """List all available endpoint tokens and their descriptions."""
        endpoints = {}
        for token, item in self.mapping.items():
            if isinstance(item, str):
                # Extract description from legacy endpoints
                lines = item.split("\n")
                for line in lines:
                    if "def " in line and "_endpoint" in line:
                        endpoints[token] = f"Legacy endpoint: {line.strip()}"
                        break
            else:
                # Module-based endpoint
                if hasattr(item, "__doc__") and item.__doc__:
                    endpoints[token] = item.__doc__.strip()
                else:
                    endpoints[token] = f"Endpoint module: {token}"
        return endpoints


# REST API for compilation service
MAX_FILE_BYTES = int(os.getenv("TRANSLATE_MAX_FILE_BYTES", "1048576"))
BATCH_MAX_WORKERS = int(os.getenv("TRANSLATE_BATCH_MAX_WORKERS", "4"))
CACHE_TTL_SECONDS = int(os.getenv("TRANSLATE_CACHE_TTL_SECONDS", "1800"))
CACHE_MAXSIZE = int(os.getenv("TRANSLATE_CACHE_MAXSIZE", "256"))


def _compute_mapping_version() -> str:
    # Stable hash to invalidate caches when mapping changes
    items = []
    for k in sorted(legacy_mapping.keys()):
        items.append(k)
        items.append(legacy_mapping[k])
    digest = sha256("\u0001".join(items).encode("utf-8")).hexdigest()
    return digest


MAPPING_VERSION = _compute_mapping_version()


def _read_text_with_limits(path: str, max_bytes: int = MAX_FILE_BYTES) -> str:
    p = Path(path)
    if not p.exists():
        raise HTTPException(
            status_code=404, detail={"code": "file_not_found", "path": str(path)}
        )
    try:
        size = p.stat().st_size
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail={"code": "file_stat_error", "path": str(path), "error": str(exc)},
        )
    if size > max_bytes:
        raise HTTPException(
            status_code=413,
            detail={
                "code": "file_too_large",
                "path": str(path),
                "bytes": size,
                "limit": max_bytes,
            },
        )
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, detail={"code": "file_not_found", "path": str(path)}
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail={"code": "file_read_error", "path": str(path), "error": str(exc)},
        )


def _ensure_output_parent_exists(path: str):
    parent = Path(path).parent
    if not parent.exists():
        raise HTTPException(
            status_code=404,
            detail={"code": "output_dir_not_found", "path": str(parent)},
        )


def _validate_tokens(tokens: List[str], mapping_keys: List[str]):
    if not isinstance(tokens, list) or any(not isinstance(t, str) for t in tokens):
        raise HTTPException(
            status_code=400,
            detail={
                "code": "invalid_tokens_type",
                "message": "tokens must be a list of strings",
            },
        )
    unknown = [t for t in tokens if t not in mapping_keys]
    if unknown:
        raise HTTPException(
            status_code=400, detail={"code": "unknown_tokens", "unknown": unknown}
        )


class SimpleTTLCache:
    def __init__(self, maxsize: int = CACHE_MAXSIZE, ttl: int = CACHE_TTL_SECONDS):
        self.maxsize = maxsize
        self.ttl = ttl
        self._store = {}
        self._lock = threading.Lock()

    def get(self, key):
        with self._lock:
            item = self._store.get(key)
            if not item:
                return None
            value, expiry = item
            if expiry < time():
                self._store.pop(key, None)
                return None
            return value

    def set(self, key, value):
        with self._lock:
            if len(self._store) >= self.maxsize:
                # naive eviction: pop an arbitrary item
                self._store.pop(next(iter(self._store)))
            self._store[key] = (value, time() + self.ttl)


TOKENS_TO_CODE_CACHE = SimpleTTLCache()
CODE_TO_TOKENS_CACHE = SimpleTTLCache()


def _key_tokens(tokens: List[str], include_imports: bool) -> str:
    raw = "|".join(tokens) + f"|imports={include_imports}|v={MAPPING_VERSION}"
    return sha256(raw.encode("utf-8")).hexdigest()


def _key_code(code: str) -> str:
    raw = sha256(code.encode("utf-8")).hexdigest() + f"|v={MAPPING_VERSION}"
    return sha256(raw.encode("utf-8")).hexdigest()


# Global compiler instance for reuse
GLOBAL_COMPILER = None


def _get_compiler() -> "BackendCompiler":
    global GLOBAL_COMPILER
    if GLOBAL_COMPILER is None:
        GLOBAL_COMPILER = BackendCompiler()
    return GLOBAL_COMPILER


if __name__ == "__main__":
    compiler = BackendCompiler()
    compiler.file_tokens_to_code("input.txt", "output.py")
