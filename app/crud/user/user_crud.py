from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .user_utils import get_hashed_password
from app.schemas import UserCreateRequest, UserResponse, UserResponseWithRecentVideo
from app import models
from datetime import date, datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserCreateRequest) -> int:
    plain_password = user.password
    hashed_password = get_hashed_password(plain_password)
    birthday: date = datetime.strptime(user.birthday, "%Y-%m-%d")
    if user.username == 'joonwan':
        db_user = models.User(username=user.username, name=user.name, hashed_password=hashed_password, email=user.email,
                              birthday=birthday, authority="ROLE_ADMIN")
    else:
        db_user = models.User(username=user.username, name=user.name, hashed_password=hashed_password, email=user.email,
                              birthday=birthday, authority="ROLE_USER")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.id


## for admin user
def find_by_id(db: Session, id: int) -> UserResponse:
    find_user: models.User = db.query(models.User).filter(models.User.id == id).first()
    username = find_user.username
    authority: str = find_user.authority
    return UserResponse(id=id, username=username, authority=authority, hashed_password=find_user.hashed_password)


def find_by_id_with_recent_video(db: Session, id: int) -> UserResponseWithRecentVideo:
    find_user: models.User = db.query(models.User).filter(models.User.id == id).first()
    return UserResponseWithRecentVideo(
        id=find_user.id,
        username=find_user.username,
        authority=find_user.authority,
        recent_videos=find_user.recent_videos
    )


def find_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()



def find_all(db: Session) -> list[UserResponse]:
    result_list = []
    users: list[type[models.User]] = db.query(models.User).all()
    for user in users:
        result_list.append(UserResponse(id=user.id, username=user.username, authority=user.authority,
                                        hashed_password=user.hashed_password))
    return result_list


def delete_by_id(db: Session, id: int) -> None:
    find_user: models.User = db.query(models.User).filter(models.User.id == id).first()
    if find_user:
        db.delete(find_user)
        db.commit()


def delete_all(db: Session) -> None:
    users: list[UserResponse] = find_all(db)
    for user in users:
        delete_by_id(db, user.id)
