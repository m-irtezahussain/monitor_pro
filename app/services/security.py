import bcrypt

from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from app.config.settings import settings


def hash_password(password: str) -> bytes:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    return hashed

def verify_password(password: str, hash: str) -> bool:
    try:
        check = bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
    except (ValueError, TypeError):
        return False


def create_access_token(user_id: int, user_name: str, user_email: str) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "name": user_name,
        "email": user_email,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes)
    }

    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token

def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm],)
    except InvalidTokenError:
        raise ValueError("Invalid Token")
    except  ExpiredSignatureError:
        raise ValueError("Token Expired")
    
    if payload.get("type") != "access":
        raise ValueError("Invalid Token Type")
    
    return payload

def create_refresh_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(days=settings.refresh_token_expire_days)
    }

    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token

def decode_refresh_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm],)
    except InvalidTokenError:
        raise ValueError("Invalid Refresh Token")
    except  ExpiredSignatureError:
        raise ValueError("Refresh Token Expired")
    
    if payload.get("type") != "refresh":
        raise ValueError("Invalid Token Type")
    
    return payload
    





