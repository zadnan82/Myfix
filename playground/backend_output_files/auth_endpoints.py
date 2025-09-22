
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

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database Models
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

# Auto-create tables on startup (dev convenience)
Base.metadata.create_all(bind=engine)

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

# Pydantic models
class User(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    created_at: datetime
    is_active: bool

@app.post("/register")
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

@app.post("/login")
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

@app.get("/me", response_model=UserResponse)
def me_endpoint(current_user: UserDB = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Requires valid session token in Authorization header.
    """
    return current_user

@app.post("/logout")
def logout_endpoint(session: SessionDB = Depends(get_current_session), db: Session = Depends(get_db)):
    """
    Logout current user by destroying their session.
    
    Requires valid session token in Authorization header.
    """
    db.delete(session)
    db.commit()
    return {"msg": "Logged out successfully"}

