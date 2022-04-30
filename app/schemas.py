from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    user_id: int

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    title: str

    class Config:
        orm_mode = True


class UpdateCreate(PostBase):
    pass


class PostResponse(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
