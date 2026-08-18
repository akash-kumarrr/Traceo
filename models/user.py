from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer, Float
from .base import Base

class User(Base) :
    __tablename__ = "users"
    full_name : Mapped[str] = mapped_column(String)
    email : Mapped[str] = mapped_column(String, unique=True)
    hashed_password : Mapped[str] = mapped_column(String)
    username : Mapped[str] = mapped_column(String, unique=True)
    longitude : Mapped[float] = mapped_column(Float)
    latitude : Mapped[float] = mapped_column(Float)
    city : Mapped[str] = mapped_column(String)
    state : Mapped[str] = mapped_column(String)
    country : Mapped[str] = mapped_column(String)