from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.crud.musicvideo import find_all, save_music_video
from app.database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    tags=["music_videos"],
    prefix="/music_videos"
)


@router.get("/")
async def get_music_videos(db: Session = Depends(get_db)):
    return find_all(db=db)

# @router.get("/test")
# async def test():
#     def iterfile():  #
#         with open("/Users/joojeon/py/letsDance/static/music_video/thumbnail/775eb4e2-5ae5-4f13-ac04-b3ab6654b524Law_fixed.mp4.jpg", mode="rb") as file_like:  #
#             yield from file_like  #
#
#     return StreamingResponse(iterfile(), media_type="video/mp4")





