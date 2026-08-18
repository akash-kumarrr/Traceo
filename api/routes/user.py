from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserBase, UserCreate
from sqlalchemy.orm import Session
from core.database import get_db
from api.deps.user import create_user
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from core.security import verify_password, create_access_token
from api.deps.user import get_current_user
from models.user import User
from schemas.token import Token
from schemas.user import UserCreateResponse





router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def create(new_user : UserCreate, db : Session = Depends(get_db)):
    create_user(user_in=new_user, db=db)



@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = db.scalars(
        select(User).where(User.username == form_data.username)
    ).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserCreateResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Protected endpoint — only accessible with a valid Bearer token."""
    return current_user