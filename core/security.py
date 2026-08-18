from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from datetime import timedelta, datetime, timezone
from core.config import settings
import jwt

password_hash = PasswordHash((Argon2Hasher(),))

def get_password_hash(plain_password : str) -> str :
    return password_hash.hash(plain_password)

def verify_password(plain_password : str, hashed_password : str) -> bool : 
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data : dict, expire_delta : timedelta | None = None) -> str :
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expire_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp" : expire})
    return jwt.encode(to_encode, settings.app_secret_key, algorithm=settings.algorithm)