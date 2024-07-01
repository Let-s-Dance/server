from datetime import datetime

from sqlalchemy.orm import Session
from app import models


def create_recent_video(db: Session, user_id: int, mv_id: int, thumbnail_endpoint: str) -> int:
    find_recent_video: models.RecentVideo = db.query(models.RecentVideo).filter(
        models.RecentVideo.user_id == user_id).filter(
        models.RecentVideo.mv_id == mv_id).first()

    if not find_recent_video:
        db_recent_video = models.RecentVideo(user_id=user_id, mv_id=mv_id, created_at=datetime.now(),
                                             thumbnail_endpoint=thumbnail_endpoint)
        db.add(db_recent_video)
        db.commit()
        db.refresh(db_recent_video)
        return db_recent_video.id

    else:
        find_recent_video.created_at = datetime.now()
        db.commit()
        return find_recent_video.id
