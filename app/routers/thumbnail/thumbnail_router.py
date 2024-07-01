from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from app.database import SessionLocal
from app.crud.musicvideo import find_by_id
from sqlalchemy.orm import Session
from app.models import MusicVideo


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    tags=["thumbnail"],
    prefix="/thumbnail"
)


@router.get("/{mv_id}")
async def get_thumbnail(mv_id: int, db: Session = Depends(get_db)):

    find_mv: MusicVideo = find_by_id(db=db, pk=mv_id)
    return FileResponse(find_mv.thumbnail_location)

