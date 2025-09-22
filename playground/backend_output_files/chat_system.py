
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

# Chat message data model
class ChatMessageData(BaseModel):
    message: str
    chat_room: Optional[str] = "general"
    message_type: Optional[str] = "text"  # text, image, file
    reply_to: Optional[int] = None  # ID of message being replied to

# Chat room database model
class ChatRoomDB(Base):
    __tablename__ = "chat_rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_private = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Chat message database model
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

@app.post("/chat")
def chat_handler(chat_data: ChatMessageData, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Handle chat message submissions from frontend.
    
    Saves messages to database and supports chat rooms and replies.
    Requires authentication.
    """
    # Basic validation
    if not chat_data.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if len(chat_data.message) > 2000:
        raise HTTPException(status_code=400, detail="Message too long (max 2000 characters)")
    
    # Clean input
    message_content = chat_data.message.strip()
    room_name = chat_data.chat_room.strip() if chat_data.chat_room else "general"
    
    # Find or create chat room
    chat_room = db.query(ChatRoomDB).filter(ChatRoomDB.name == room_name).first()
    if not chat_room:
        # Create default chat room
        chat_room = ChatRoomDB(
            name=room_name,
            description=f"Chat room: {room_name}",
            is_private=False,
            created_by=current_user.id
        )
        db.add(chat_room)
        db.commit()
        db.refresh(chat_room)
    
    # Validate reply_to message exists if specified
    reply_to_message = None
    if chat_data.reply_to:
        reply_to_message = db.query(ChatMessageDB).filter(
            ChatMessageDB.id == chat_data.reply_to,
            ChatMessageDB.chat_room_id == chat_room.id,
            ChatMessageDB.is_deleted == False
        ).first()
        if not reply_to_message:
            raise HTTPException(status_code=404, detail="Reply target message not found")
    
    # Create chat message
    chat_message = ChatMessageDB(
        message=message_content,
        user_id=current_user.id,
        chat_room_id=chat_room.id,
        message_type=chat_data.message_type or "text",
        reply_to_id=chat_data.reply_to if reply_to_message else None
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    
    # Log chat message
    logging.info(f"Chat message sent - User: {current_user.username} Room: {room_name} Message ID: {chat_message.id}")
    
    # Prepare response with user info
    response_data = {
        "msg": "Message sent successfully",
        "message_id": chat_message.id,
        "chat_room": room_name,
        "timestamp": chat_message.created_at.isoformat(),
        "user": {
            "id": current_user.id,
            "username": current_user.username
        }
    }
    
    # Add reply context if this is a reply
    if reply_to_message:
        reply_user = db.query(UserDB).filter(UserDB.id == reply_to_message.user_id).first()
        response_data["reply_to"] = {
            "message_id": reply_to_message.id,
            "preview": reply_to_message.message[:100] + "..." if len(reply_to_message.message) > 100 else reply_to_message.message,
            "user": reply_user.username if reply_user else "Unknown"
        }
    
    return response_data

# Additional endpoint to get chat history
@app.get("/chat/history")
def get_chat_history(
    chat_room: str = "general",
    limit: int = 50,
    offset: int = 0,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get chat message history for a room.
    """
    # Find chat room
    room = db.query(ChatRoomDB).filter(ChatRoomDB.name == chat_room).first()
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")
    
    # Get messages with user info
    messages = db.query(ChatMessageDB, UserDB).join(
        UserDB, ChatMessageDB.user_id == UserDB.id
    ).filter(
        ChatMessageDB.chat_room_id == room.id,
        ChatMessageDB.is_deleted == False
    ).order_by(ChatMessageDB.created_at.desc()).offset(offset).limit(limit).all()
    
    # Format response
    message_list = []
    for msg, user in messages:
        message_data = {
            "id": msg.id,
            "message": msg.message,
            "user": {
                "id": user.id,
                "username": user.username
            },
            "timestamp": msg.created_at.isoformat(),
            "message_type": msg.message_type
        }
        
        # Add reply info if this message is a reply
        if msg.reply_to_id:
            reply_msg = db.query(ChatMessageDB, UserDB).join(
                UserDB, ChatMessageDB.user_id == UserDB.id
            ).filter(ChatMessageDB.id == msg.reply_to_id).first()
            if reply_msg:
                reply_message, reply_user = reply_msg
                message_data["reply_to"] = {
                    "message_id": reply_message.id,
                    "preview": reply_message.message[:100] + "..." if len(reply_message.message) > 100 else reply_message.message,
                    "user": reply_user.username
                }
        
        message_list.append(message_data)
    
    return {
        "messages": list(reversed(message_list)),  # Return in chronological order
        "chat_room": chat_room,
        "total_messages": len(message_list),
        "has_more": len(message_list) == limit
    }

