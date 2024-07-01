from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.login_schemas import LoginRequestDto
from app.http.session import SessionData, session
from app import models
from datetime import datetime
from app.http.session.session_utils import is_valid_session, update_session
from app.database import SessionLocal
from passlib.context import CryptContext
from app.crud.user import find_by_username
import uuid

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    tags=["login"],
    prefix="/login"
)


@router.post("")
async def login(login_dto: LoginRequestDto, request: Request, db: Session = Depends(get_db)):
    if request.cookies.get("session-id"):
        before_session_id: str = request.cookies.get("session-id")
        session_data: SessionData = session.get(before_session_id)
        if session_data:
            user_id = session_data.id
            find_user = find_by_username(db=db, username=login_dto.username)
            if not find_user:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "아이디를 다시 입력해 주세요."})
            if find_user.id == user_id and before_session_id in session.keys():
                if is_valid_session(before_session_id):
                    update_session(before_session_id)
                    session_id = before_session_id
                    response = JSONResponse(status_code=status.HTTP_200_OK, content={"details": "update session"})
                    response.set_cookie("session-id", session_id)
                    return response
                else:
                    del session[before_session_id]

    user_name: str = login_dto.username
    find_user = find_by_username(db, user_name)
    if not find_user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "아이디를 다시 입력해 주세요."})

    if not password_context.verify(login_dto.password, find_user.hashed_password):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "비밀 번호를 다시 입력해 주세요."})

    session_id = str(uuid.uuid4())
    authority = find_user.authority
    session_data: SessionData = SessionData(
        **{"id": find_user.id, "created_at": datetime.now(), "authority": authority})
    session[session_id] = session_data
    response = JSONResponse(status_code=status.HTTP_200_OK, content={"details": "success"})
    response.set_cookie("session-id", session_id)

    return response
