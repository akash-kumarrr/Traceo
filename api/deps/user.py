from schemas.user import UserBase, UserCreate, UserCreateResponse
from core.database import get_db
from fastapi import Depends, status, HTTPException
from models.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.security import get_password_hash, verify_password
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from core.database import get_db
from core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from schemas.token import TokenData

def create_user(user_in : UserCreate, db : Session = Depends(get_db)) -> UserCreateResponse:
    user_dict = user_in.model_dump(exclude={"password"})
    db_user = User(**user_dict, hashed_password=get_password_hash(user_in.password))
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user_in 
    

def read_user_by_id(id : int, db : Session = Depends(get_db)):
    try :
        return db.scalars(select(User).where(User.id == id)).first()
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except HTTPException:
        raise




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
        
    return {
        "token" : token,
        "data" : user
    }