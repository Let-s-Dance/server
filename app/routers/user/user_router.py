from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.crud.user.user_crud import find_by_id_with_recent_video
from app.http.session.session_utils import get_id_from_session
from app.schemas.user_schemas import UserResponseWithRecentVideo

from app.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    tags=["user"],
    prefix="/user"
)


@router.get("")
async def get_user(request: Request, db: Session = Depends(get_db)) -> UserResponseWithRecentVideo:
    session_id: str = request.cookies.get("session-id")
    user_id = get_id_from_session(session_id)

    find_user: UserResponseWithRecentVideo = find_by_id_with_recent_video(db=db, id=user_id)
    return find_user


