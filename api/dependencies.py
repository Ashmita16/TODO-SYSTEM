from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from config.config import settings
from db.database import get_db
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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

        if pwd_changed_at > token_issued_at:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="PASSWORD WAS CHANGED RECENTLY, PLEASE LOG IN AGAIN!"
            )

    return user
