from typing import List, Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.schemas.user_schemas import UserResponse
from starlette.responses import JSONResponse
from starlette import status
from app.crud.user import find_by_id, find_all, delete_all, delete_by_id
from app.crud.musicvideo import save_music_video
from app.database import SessionLocal
from sqlalchemy.orm import Session
from .admin_utils import validate_file


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    tags=["admin"],
    prefix="/admin"
)


@router.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    find_user: UserResponse = find_by_id(db=db, id=user_id)
    return find_user


@router.get("/users")
async def get_users(db: Session = Depends(get_db)) -> List[UserResponse]:
    return find_all(db=db)


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    delete_by_id(db=db, id=user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"details": "success"})


@router.delete("/users")
async def delete_all_user(db: Session = Depends(get_db)) -> JSONResponse:
    delete_all(db=db)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"details": "success"})


@router.post("/music_videos")
async def upload_music_video(
        file: Annotated[UploadFile, File()],
        title: Annotated[str, Form()],
        musician: Annotated[str, Form()],
        db: Session = Depends(get_db)
):
    if not validate_file(file, title, musician):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"details": "입력값이 빌수 없습니다."})

    await save_music_video(db, title, musician, file)
    return JSONResponse(status_code=200, content={"details": "success"})
