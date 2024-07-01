from typing import Type

from sqlalchemy.orm import Session

from app.models import MusicVideo
from fastapi import UploadFile
from app import models
from static.music_video.video.abspath import get_abs_path_video
from static.music_video.thumbnail.abspath import get_abs_path_thumbnail
import uuid
import os, cv2

VIDEO_DIR = get_abs_path_video()
THUMBNAIL_DIR = get_abs_path_thumbnail()


async def save_music_video(db: Session, title: str, musician: str, file: UploadFile) -> int:
    f_name = str(uuid.uuid4()) + file.filename
    video_location = f"{VIDEO_DIR}/{f_name}"
    thumbnail_location = f"{THUMBNAIL_DIR}/{f_name}.jpg"
    content = await file.read()
    with open(os.path.join(VIDEO_DIR, f_name), "wb") as f:
        f.write(content)

    cap = cv2.VideoCapture(video_location)
    retval, frame = cap.read()
    cv2.imwrite(thumbnail_location, frame)

    db_music_video = models.MusicVideo(name=title, musician=musician,
                                       file_location=video_location, thumbnail_location=thumbnail_location)
    db.add(db_music_video)
    db.commit()
    db.refresh(db_music_video)
    return db_music_video.id


def find_by_id(db: Session, pk: int) -> MusicVideo:
    return db.query(models.MusicVideo).filter(models.MusicVideo.id == pk).first()


def find_all(db: Session) -> list[Type[MusicVideo]]:
    return db.query(models.MusicVideo).all()


def delete_music_video(db: Session, pk: int) -> None:
    find_music_video: models.MusicVideo = find_by_id(db, pk)
    db.delete(find_music_video)
