
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

# Contact form data model
class ContactFormData(BaseModel):
    name: str
    email: str
    subject: Optional[str] = None
    message: str

# Contact form database model
class ContactFormDB(Base):
    __tablename__ = "contact_forms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)

@app.post("/contact")
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

# Login form data model (more flexible than core User model)
class LoginFormData(BaseModel):
    username: str
    password: str
    remember_me: Optional[bool] = False

@app.post("/login-form")
def login_form_handler(form_data: LoginFormData, db: Session = Depends(get_db)):
    """
    Handle login form submissions from frontend.
    
    More user-friendly version of core login endpoint with better error messages.
    """
    # Basic validation
    if not form_data.username.strip():
        raise HTTPException(status_code=400, detail="Username is required")
    if not form_data.password:
        raise HTTPException(status_code=400, detail="Password is required")
    
    # Clean username (remove whitespace, convert to lowercase)
    username = form_data.username.strip().lower()
    
    # Find user
    db_user = db.query(UserDB).filter(UserDB.username == username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Check if user is active
    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")
    
    # Verify password
    if not pwd_context.verify(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Create session with extended expiry if remember_me is checked
    session_id = str(uuid.uuid4())
    expiry_hours = 24 * 7 if form_data.remember_me else 1  # 7 days vs 1 hour
    expiry = datetime.utcnow() + timedelta(hours=expiry_hours)
    
    db.add(SessionDB(id=session_id, user_id=db_user.id, expiry=expiry))
    db.commit()
    
    # Log successful login
    logging.info(f"User {db_user.username} logged in successfully - Session: {session_id}")
    
    return {
        "msg": "Login successful",
        "session_token": session_id,
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email
        },
        "expires_in_hours": expiry_hours
    }

# Register form data model
class RegisterFormData(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str
    accept_terms: Optional[bool] = False

@app.post("/register-form")
def register_form_handler(form_data: RegisterFormData, db: Session = Depends(get_db)):
    """
    Handle registration form submissions from frontend.
    
    Enhanced validation and user-friendly error messages for web forms.
    """
    # Basic validation
    if not form_data.username.strip():
        raise HTTPException(status_code=400, detail="Username is required")
    if not form_data.email.strip():
        raise HTTPException(status_code=400, detail="Email is required")
    if not form_data.password:
        raise HTTPException(status_code=400, detail="Password is required")
    if not form_data.confirm_password:
        raise HTTPException(status_code=400, detail="Please confirm your password")
    
    # Password confirmation check
    if form_data.password != form_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Password strength validation
    if len(form_data.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    
    # Email format validation
    import re
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", form_data.email):
        raise HTTPException(status_code=400, detail="Please enter a valid email address")
    
    # Username validation (alphanumeric and underscore only)
    if not re.match(r"^[a-zA-Z0-9_]{3,20}$", form_data.username):
        raise HTTPException(status_code=400, detail="Username must be 3-20 characters, letters, numbers and underscore only")
    
    # Terms acceptance (optional but recommended)
    if not form_data.accept_terms:
        raise HTTPException(status_code=400, detail="Please accept the terms and conditions")
    
    # Clean input
    username = form_data.username.strip().lower()
    email = form_data.email.strip().lower()
    
    # Check if username already exists
    existing_username = db.query(UserDB).filter(UserDB.username == username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username is already taken")
    
    # Check if email already exists
    existing_email = db.query(UserDB).filter(UserDB.email == email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    # Create user
    hashed_password = pwd_context.hash(form_data.password)
    db_user = UserDB(
        username=username,
        email=email,
        password=hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Log successful registration
    logging.info(f"New user registered: {username} ({email}) - ID: {db_user.id}")
    
    return {
        "msg": "Account created successfully! You can now log in.",
        "user_id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "status": "active"
    }

# Email form data model
class EmailFormData(BaseModel):
    to: str
    subject: str
    message: str
    from_name: Optional[str] = None

# Email log database model
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

@app.post("/send-email")
def email_form_handler(email_data: EmailFormData, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Handle email form submissions from frontend.
    
    Validates email, sends via SMTP, and logs the transaction.
    Requires authentication to prevent spam.
    """
    # Basic validation
    if not email_data.to.strip():
        raise HTTPException(status_code=400, detail="Recipient email is required")
    if not email_data.subject.strip():
        raise HTTPException(status_code=400, detail="Subject is required")
    if not email_data.message.strip():
        raise HTTPException(status_code=400, detail="Message is required")
    
    # Email format validation
    import re
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email_data.to.strip()):
        raise HTTPException(status_code=400, detail="Invalid recipient email format")
    
    # Clean input
    to_email = email_data.to.strip().lower()
    subject = email_data.subject.strip()
    message = email_data.message.strip()
    from_name = email_data.from_name.strip() if email_data.from_name else current_user.username
    
    # Create email log entry
    email_log = EmailLogDB(
        to_email=to_email,
        from_email=current_user.email,
        from_name=from_name,
        subject=subject,
        message=message,
        status="pending"
    )
    db.add(email_log)
    db.commit()
    db.refresh(email_log)
    
    try:
        # Email sending configuration (environment variables)
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        smtp_server = os.getenv("SMTP_SERVER", "localhost")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_username = os.getenv("SMTP_USERNAME", "")
        smtp_password = os.getenv("SMTP_PASSWORD", "")
        smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        
        # Create message
        msg = MIMEMultipart()
        msg["From"] = f"{from_name} <{smtp_username or current_user.email}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        
        # Add message body
        msg.attach(MIMEText(message, "plain"))
        
        # Send email
        if smtp_server != "localhost" and smtp_username:
            server = smtplib.SMTP(smtp_server, smtp_port)
            if smtp_use_tls:
                server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username or current_user.email, to_email, msg.as_string())
            server.quit()
            
            # Update log as sent
            email_log.status = "sent"
            email_log.sent_at = datetime.utcnow()
            status_message = "Email sent successfully"
        else:
            # Development mode - just log
            email_log.status = "sent"
            email_log.sent_at = datetime.utcnow()
            status_message = "Email logged (development mode - no SMTP configured)"
            
    except Exception as e:
        # Update log with error
        email_log.status = "failed"
        email_log.error_message = str(e)
        status_message = f"Failed to send email: {str(e)}"
        logging.error(f"Email sending failed for log ID {email_log.id}: {str(e)}")
        
    finally:
        db.commit()
    
    # Log the email attempt
    logging.info(f"Email {email_log.status} - From: {current_user.email} To: {to_email} Subject: {subject} - Log ID: {email_log.id}")
    
    return {
        "msg": status_message,
        "email_id": email_log.id,
        "status": email_log.status,
        "to": to_email,
        "subject": subject
    }

