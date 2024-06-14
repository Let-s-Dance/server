from sqlalchemy.orm import Session
from ... import models, schemas


def create_music(db: Session, music: schemas.MusicCreate) -> models.Music:
    db_music = models.Music(name=music.name, musician=music.musician, file_location= music.file_location)
    db.add(db_music)
    db.commit()
    db.refresh(db_music)
    return db_music


def get_musics_by_name(db: Session, music_name: str) -> list[models.Music]:
    return db.query(models.Music).filter(models.Music.name == music_name).all()


def get_music_by_id(db: Session, music_id: int) -> models.Music:
    return db.query(models.Music).filter(models.Music.id == music_id).first()


def get_music__by_musician(db: Session, musician: str) -> list[models.Music]:
    return db.query(models.Music).filter(models.Music.musician == musician).all()


def delete_music(db: Session, music_id: int) -> None:
    return db.query(models.Music).filter(models.Music.id == music_id).delete()
