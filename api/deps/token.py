import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from core.database import get_db
from core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from schemas.token import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)) :
    creadential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate" : "Bearer"},
    )

    try : 
        payload = jwt.decode(token, settings.app_secret_key, algorithms=[settings.algorithm])
        username : str = payload.get("sub")
        if username is None :
            raise creadential_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError :
        raise creadential_exception
    
    user = db.scalars(
        select(User).where(User.username == token_data.username)
    ).first()
    
    if user is None:
        raise creadential_exception
        
    return 