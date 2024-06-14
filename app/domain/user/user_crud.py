from sqlalchemy.orm import Session
from datetime import date, datetime
from ... import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# create user

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    birthday: date = datetime.strptime(user.birthday, "%Y-%m-%d")
    db_user = models.User(user_real_name=user.user_real_name, user_name=user.user_name,
                          hashed_password=hashed_password, email=user.email, birthday=birthday)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# read user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):
    return db.query(models.User).all()


def get_users_by_user_name(db: Session, user_name: str) -> models.User:
    return db.query(models.User).filter(models.User.user_name == user_name).first()


# delete

def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return user_id
