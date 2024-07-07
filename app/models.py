from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    name: str
    email: str
    hashed_password: str

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None

class UserRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class EmailSchema(BaseModel):
    email: EmailStr
