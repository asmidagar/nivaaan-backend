from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    name: str
    email: str          # ← changed from EmailStr to str
    password: str


class UserLogin(BaseModel):
    email: str          # ← changed from EmailStr to str
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: Optional[datetime] = None


class UserInDB(BaseModel):
    name: str
    email: str
    password: str
    created_at: datetime