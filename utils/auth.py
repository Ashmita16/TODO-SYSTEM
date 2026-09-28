from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from jose import jwt
from config.config import settings

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError):
        return False

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    now_utc = datetime.now(timezone.utc)
    
    expire = now_utc + (
        expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    to_encode.update({
        "iat": int(now_utc.timestamp()),
        "exp": expire
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    issued_at_ist = now_utc.astimezone(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    
    return encoded_jwt, issued_at_ist