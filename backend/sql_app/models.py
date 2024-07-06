from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    videos = relationship("Video", back_populates="user")

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String, unique=True)
    summary = Column(String)

    comments = relationship("VideoComment", back_populates="video")
    user = relationship("User", back_populates="videos")

class VideoComment(Base):
    __tablename__ = 'video_comments'

    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    summary = Column(String)
    category_count = Column(Integer)
    comment_insights = Column(String)  # Store as JSON string
    representative_comments = Column(String)  # Store as JSON string

    video = relationship("Video", back_populates="comments")