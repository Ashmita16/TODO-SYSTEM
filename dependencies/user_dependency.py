from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from config.config import settings
from dependencies.db_dependency import get_db
from models.user import User

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        iat: int = payload.get("iat")
        
        if username is None or iat is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    if user.password_changed_at is not None:
        token_issued_at = datetime.fromtimestamp(iat, tz=timezone.utc)
        pwd_changed_at = user.password_changed_at

        if pwd_changed_at.tzinfo is None:
            pwd_changed_at = pwd_changed_at.replace(tzinfo=timezone.utc)
        else:
            pwd_changed_at = pwd_changed_at.astimezone(timezone.utc)

        pwd_changed_at = pwd_changed_at.replace(microsecond=0)

        if pwd_changed_at > token_issued_at:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="PASSWORD WAS CHANGED RECENTLY. PLEASE LOG IN AGAIN!"
            )

    return user