from pydantic import BaseModel, EmailStr, Field
import uuid
import datetime

class UserBase(BaseModel):
    full_name : str
    email : EmailStr
    username : str
    longitude : float
    latitude : float 
    state : str
    country : str
    city : str

class UserCreate(UserBase):
    password : str 

    class Config:
        from_attributes = True 

class UserCreateResponse(UserBase):
    id : uuid.UUID
    created_on : datetime.datetime
    updated_on : datetime.datetime

    class Config:
        from_attributes = True