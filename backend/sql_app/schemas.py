from pydantic import BaseModel, EmailStr
from typing import List, Optional

class VideoCommentBase(BaseModel):
    summary: Optional[str] = None
    category_count: Optional[int] = None
    comment_insights: Optional[str] = None  # JSON string
    representative_comments: Optional[str] = None  # JSON string

class VideoCommentCreate(VideoCommentBase):
    video_id: int

class VideoComment(VideoCommentBase):
    id: int
    video_id: int

    class Config:
        orm_mode: True

class VideoBase(BaseModel):
    url: Optional[str] = None
    summary: Optional[str] = None

class VideoCreate(VideoBase):
    user_id: int

class Video(VideoBase):
    id: int
    user_id: int
    comments: List[VideoComment] = []

    class Config:
        orm_mode: True

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    hashed_password: str
    videos: List[Video] = []

    class Config:
        orm_mode: True
