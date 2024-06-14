import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette import status
from passlib.context import CryptContext
from .. import models, schemas
from ..domain.user import user_crud
from ..database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

session = {}

white_list_get = ["/docs", "/openapi.json"]
white_list_post = ["/login", "/users"]


def is_valid_session(session_id: str) -> bool:
    if session_id not in session.keys():
        return False
    session_data: schemas.SessionData = session.get(session_id)
    updated_at = session_data.time
    now = datetime.now()

    diff = now - updated_at
    print(updated_at, now, diff)
    if diff.total_seconds() > 1800:
        return False

    return True


def update_session(session_id: str) -> None:
    session_data: schemas.SessionData = session.get(session_id)
    session_data.time = datetime.now()
    session[session_id] = session_data


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    tags=["login"]
)


@router.post("/login")
def login(login_dto: schemas.UserLogin, request: Request, db: Session = Depends(get_db)):
    if request.cookies.get("session-id"):
        before_session_id = request.cookies.get("session-id")
        session_data: schemas.SessionData = session.get(before_session_id)
        if session_data:
            user_id = session_data.user_id
            find_user: models.User = db.query(models.User).filter(models.User.user_name == login_dto.user_name).first()
            if find_user.id == user_id and before_session_id in session.keys():
                if is_valid_session(before_session_id):
                    update_session(before_session_id)
                    session_id = before_session_id
                    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
                    response.set_cookie("session-id", session_id)
                    return response
                else:
                    del session[before_session_id]

    user_name = login_dto.user_name
    find_user = user_crud.get_users_by_user_name(db, user_name)
    if not find_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="아이디를 다시 입력해 주세요.")

    if not password_context.verify(login_dto.password, find_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="비밀번호가 일치하지 않습니다.")

    session_id = str(uuid.uuid4())

    session_data: schemas.SessionData = schemas.SessionData(**{"user_id": find_user.id, "time": datetime.now()})
    session[session_id] = session_data
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie("session-id", session_id)

    return response
