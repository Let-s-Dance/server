import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette import status

from .. import models, schemas
from ..database import SessionLocal, engine
from ..schemas import MusicCreateDto

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    tags=["music"]
)


@router.post("/musics")
async def create_music(music: schemas.MusicCreateDto, db: Session = Depends(get_db)):
    if not validate(music):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="입력 값이 올바르지 않습니다.")
    upload_file: UploadFile = music.file
    file_location: str = get_file_location(upload_file)
    music_create = schemas.MusicCreate(
        **{"name": music.name, "musician": music.musician, "file_location": file_location})


def get_file_location(upload_file: UploadFile) -> str:
    name: str = upload_file.filename
    salt: str = str(uuid.uuid4())
    salted_name: str = salt + name
    return f"files/{salted_name}"


def validate(music: schemas.MusicCreateDto) -> bool:
    name: str = music.name
    musician: str = music.musician
    upload_file: UploadFile = music.file

    if name == "" or not name:
        return False

    if musician == "" or not musician:
        return False

    if not upload_file:
        return False

    return True
