from sqlalchemy.orm import Session
from . import models, schemas

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Video CRUD operations
def get_video(db: Session, video_id: int):
    return db.query(models.Video).filter(models.Video.id == video_id).first()

def get_videos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Video).offset(skip).limit(limit).all()

def create_video(db: Session, video: schemas.VideoCreate):
    db_video = models.Video(user_id=video.user_id, url=video.url, summary=video.summary)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

def get_videos_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Video).filter(models.Video.user_id == user_id).offset(skip).limit(limit).all()

# VideoComment CRUD operations
def get_video_comment(db: Session, comment_id: int):
    return db.query(models.VideoComment).filter(models.VideoComment.id == comment_id).first()

def get_video_comments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.VideoComment).offset(skip).limit(limit).all()

def get_video_comments_by_video(db: Session, video_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.VideoComment).filter(models.VideoComment.video_id == video_id).offset(skip).limit(limit).all()

def create_video_comment(db: Session, video_comment: schemas.VideoCommentCreate):
    db_video_comment = models.VideoComment(
        video_id=video_comment.video_id,
        summary=video_comment.summary,
        category_count=video_comment.category_count,
        comment_insights=video_comment.comment_insights,
        representative_comments=video_comment.representative_comments
    )
    db.add(db_video_comment)
    db.commit()
    db.refresh(db_video_comment)
    return db_video_comment
