from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.config import settings
import hashlib
from fastapi import HTTPException

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

def create_access_token(email: str, expires_delta: int = 30):
    """Creates a signed JWT with an expiration time."""

    email += settings.USER_ID_SALT
    email_hash = hashlib.sha256(email.encode()).hexdigest()[:12]

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)

    to_encode = {
        "user_id": email_hash,
        "exp": expire
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    """Decodes and validates the token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token has expired") 
    except JWTError:
        raise HTTPException(401, "Invalid token")
