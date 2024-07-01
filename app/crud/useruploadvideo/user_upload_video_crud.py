from sqlalchemy.orm import Session
from app import models
from fastapi import UploadFile
import uuid, os
from datetime import datetime
from static.upload_video.abspath import get_abs_path

DIR = get_abs_path()


async def upload_user_video(db: Session, user_id: int, mv_id: int, score: int, file: UploadFile):
    f_name = str(uuid.uuid4()) + file.filename
    file_location = f"{DIR}/{f_name}"
    content = await file.read()
    with open(os.path.join(DIR, f_name), "wb") as f:
        f.write(content)

    db_upload_video = models.UserUploadVideo(user_id=user_id, file_location=file_location, mv_id=mv_id, score=score)
    db.add(db_upload_video)
    db.commit()
    db.refresh(db_upload_video)
