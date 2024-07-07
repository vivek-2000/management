# app/models.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List


class User(BaseModel):
    username: str
    email: str
    project_id: int

class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class EmailSchema(BaseModel):
   email: List[EmailStr]