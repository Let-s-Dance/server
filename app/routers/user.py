from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .. import models, schemas
from ..domain.user import user_crud
from ..database import SessionLocal, engine
import re

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    tags=["users"]
)


@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_crud.get_user(db, user_id)


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return user_crud.get_users(db)


@router.post("/users", status_code=status.HTTP_201_CREATED)
def join(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not validate_empty_value(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="빈 값을 입력할 수 없습니다.")
    if not validate_email(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이메일 형식이 잘못 되었습니다.")
    if not validate_birthday(user.birthday):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="날짜 형식은 yyyy-mm-dd 입니다.")
    find_user = user_crud.get_users_by_user_name(db, user.user_name)
    if find_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 아이디 입니다..")
    user_crud.create_user(db, user)


def validate_empty_value(user: schemas.UserCreate):
    user_name = user.user_name
    user_real_name = user.user_real_name
    password = user.password
    email = user.email
    birthday = str(user.birthday)
    if user_name == "" or password == "" or email == "" or birthday == "" or user_real_name == "":
        return False
    return True


def validate_email(email: str):
    pattern: str = r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.fullmatch(pattern, email)


def validate_birthday(birthday: str):
    pattern: str = r"\d{4}-\d{2}-\d{2}"
    return re.fullmatch(pattern, birthday)


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    find_user = user_crud.get_user(db, user_id)
    if not find_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    user_crud.delete_user(db, user_id)
