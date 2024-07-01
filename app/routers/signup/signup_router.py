from fastapi import APIRouter, Depends
from app.schemas.user_schemas import UserCreateRequest, UserResponse
from app.crud.user import find_by_username
from starlette.responses import JSONResponse
from starlette import status
from app.crud.user import create_user
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.routers.admin.admin_utils import validate


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    tags=["signup"],
    prefix="/signup"
)


@router.post("")
async def join(user: UserCreateRequest, db: Session = Depends(get_db)) -> JSONResponse:
    if not validate(user):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"details": "다시 입력해 주세요"})
    username: str = user.username
    find_user = find_by_username(db=db, username=username)
    if find_user is not None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"details": "이미 존재하는 회원입니다."})
    create_user(db=db, user=user)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"details": "success"})
