# sevdo_backend/endpoints/newsletter_handler.py
"""
Newsletter handler endpoint - processes newsletter subscription requests.
"""


def render_endpoint(args=None, props=None):
    """
    Render newsletter subscription endpoint code.

    Args:
        args: String arguments from DSL (optional path parameters)
        props: Dictionary of properties from DSL

    Returns:
        String containing FastAPI endpoint code
    """
    # Default values
    endpoint_path = props.get("path", "/api/newsletter") if props else "/api/newsletter"
    method = props.get("method", "POST").upper() if props else "POST"

    # Support for inline args parsing if needed
    if args:
        # Could parse custom path or options from args
        pass

    # Generate the newsletter handler endpoint code
    endpoint_code = f'''
# Newsletter subscription data model
class NewsletterSubscriptionData(BaseModel):
    email: str
    name: Optional[str] = None

@app.{method.lower()}("{endpoint_path}")
def newsletter_handler(subscription_data: NewsletterSubscriptionData, db: Session = Depends(get_db)):
    """
    Handle newsletter subscription requests.
    
    Validates email, checks for existing subscription, and saves to database.
    """
    # Basic validation
    if not subscription_data.email.strip():
        raise HTTPException(status_code=400, detail="Email address is required")
    
    # Email format validation (simple approach)
    email = subscription_data.email.strip().lower()
    
    if not email or '@' not in email or '.' not in email.split('@')[1]:
        raise HTTPException(status_code=400, detail="Invalid email address format")
    
    # Check if email already subscribed
    existing_subscriber = db.query(NewsletterSubscriberDB).filter(
        NewsletterSubscriberDB.email == email
    ).first()
    
    if existing_subscriber:
        if existing_subscriber.is_active:
            return {{
                "msg": "You're already subscribed to our newsletter!",
                "status": "already_subscribed",
                "email": email
            }}
        else:
            # Reactivate inactive subscription
            existing_subscriber.is_active = True
            existing_subscriber.subscribed_at = datetime.utcnow()
            db.commit()
            
            logging.info(f"Newsletter subscription reactivated: {{email}}")
            
            return {{
                "msg": "Welcome back! Your newsletter subscription has been reactivated.",
                "status": "reactivated",
                "email": email
            }}
    
    # Create new subscription
    import uuid
    unsubscribe_token = str(uuid.uuid4())
    
    new_subscriber = NewsletterSubscriberDB(
        email=email,
        name=subscription_data.name.strip() if subscription_data.name else None,
        unsubscribe_token=unsubscribe_token
    )
    
    db.add(new_subscriber)
    db.commit()
    db.refresh(new_subscriber)
    
    # Log successful subscription
    logging.info(f"New newsletter subscription: {{email}} - ID: {{new_subscriber.id}}")
    
    return {{
        "msg": "Thank you for subscribing! You'll receive our latest updates via email.",
        "status": "subscribed",
        "email": email,
        "subscription_id": new_subscriber.id
    }}

# Unsubscribe endpoint
@app.get("{endpoint_path}/unsubscribe/{{token}}")
def newsletter_unsubscribe(token: str, db: Session = Depends(get_db)):
    """
    Handle newsletter unsubscribe requests via token.
    """
    subscriber = db.query(NewsletterSubscriberDB).filter(
        NewsletterSubscriberDB.unsubscribe_token == token
    ).first()
    
    if not subscriber:
        raise HTTPException(status_code=404, detail="Invalid unsubscribe link")
    
    if not subscriber.is_active:
        return {{
            "msg": "You have already unsubscribed from our newsletter.",
            "status": "already_unsubscribed"
        }}
    
    subscriber.is_active = False
    db.commit()
    
    logging.info(f"Newsletter unsubscribe: {{subscriber.email}} - ID: {{subscriber.id}}")
    
    return {{
        "msg": "You have been successfully unsubscribed from our newsletter.",
        "status": "unsubscribed",
        "email": subscriber.email
    }}

# Get newsletter stats (optional admin endpoint)
@app.get("{endpoint_path}/stats")
def newsletter_stats(current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get newsletter subscription statistics (requires authentication).
    """
    total_subscribers = db.query(NewsletterSubscriberDB).count()
    active_subscribers = db.query(NewsletterSubscriberDB).filter(
        NewsletterSubscriberDB.is_active == True
    ).count()
    
    recent_subscribers = db.query(NewsletterSubscriberDB).filter(
        NewsletterSubscriberDB.subscribed_at >= datetime.utcnow() - timedelta(days=30),
        NewsletterSubscriberDB.is_active == True
    ).count()
    
    return {{
        "total_subscribers": total_subscribers,
        "active_subscribers": active_subscribers,
        "recent_subscribers_30days": recent_subscribers,
        "unsubscribed": total_subscribers - active_subscribers
    }}'''

    return endpoint_code.strip()


# Register with token "nlh"
ENDPOINT_TOKEN = "nlh"
