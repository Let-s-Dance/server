from fastapi import APIRouter, Depends, UploadFile, status
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.database import SessionLocal
from app.http.session import session, SessionData
from app.crud.useruploadvideo import upload_user_video
from app.crud.recentvideo.recent_video_crud import create_recent_video


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    tags=["game"],
    prefix="/game"
)

PATH = "http://127.0.0.1:8000"

@router.post("/music_videos/{mv_id}")
async def play_game(mv_id: int, request: Request, file: UploadFile, db: Session = Depends(get_db)):

    session_id: str = request.cookies.get("session-id")
    session_data: SessionData = session.get(session_id)
    user_id: int = session_data.id

    thumbnail_endpoint: str = f"{PATH}/thumbnail/{mv_id}"
    create_recent_video(db=db, user_id=user_id, mv_id=mv_id, thumbnail_endpoint=thumbnail_endpoint)

    ###
    ## 외부 api 연동 section -> score 반환받음
    score = 10
    ###
    await upload_user_video(db=db, user_id=user_id, mv_id=mv_id, score=score, file=file)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"details": "success"})
