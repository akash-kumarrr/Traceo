from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import settings
from fastapi import HTTPException, status

engine = create_engine(
    settings.db_url,
    connect_args={"check_same_thread" : False}
)

SessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False
)

def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally :
        db.close()