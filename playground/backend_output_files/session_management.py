
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

@app.post("/refresh")
def refresh_endpoint(session: SessionDB = Depends(get_current_session), db: Session = Depends(get_db)):
    """
    Refresh current session with new token.
    
    Generates new session ID and extends expiry time.
    Requires valid session token in Authorization header.
    """
    new_session_id = str(uuid.uuid4())
    session.id = new_session_id
    session.expiry = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    return {"session_token": new_session_id}

@app.post("/logout-all")
def logout_all_endpoint(current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Logout from all sessions for current user.
    
    Deletes all active sessions belonging to the authenticated user.
    Requires valid session token in Authorization header.
    """
    db.query(SessionDB).filter(SessionDB.user_id == current_user.id).delete()
    db.commit()
    return {"msg": "Logged out of all sessions"}

@app.get("/sessions")
def list_sessions_endpoint(current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    List all active sessions for current user.
    
    Returns session details including ID, expiry time, and creation time.
    Requires valid session token in Authorization header.
    """
    sessions = db.query(SessionDB).filter(SessionDB.user_id == current_user.id).all()
    return [{"id": s.id, "expiry": s.expiry.isoformat(), "created_at": s.created_at.isoformat()} for s in sessions]

@app.delete("/sessions/{session_id}")
def revoke_session_endpoint(session_id: str, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Revoke (delete) specific session by ID.
    
    Only allows users to revoke their own sessions.
    Requires valid session token in Authorization header.
    """
    session = db.query(SessionDB).filter(SessionDB.id == session_id, SessionDB.user_id == current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()
    return {"msg": "Session revoked successfully"}

