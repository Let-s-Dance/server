from app.schemas.user_schemas import UserCreateRequest
from fastapi import UploadFile
import re


def validate_file(file: UploadFile, title: str, musician: str) -> bool:
    if not file:
        return False
    if len(title) == 0 or len(musician) == 0:
        return False

    return True


def validate(user: UserCreateRequest) -> bool:
    if not validate_empty_value(user):
        return False
    if not validate_email(user.email):
        return False
    if not validate_birthday(user.birthday):
        return False

    return True




def validate_empty_value(user: UserCreateRequest) -> bool:
    username = user.username
    name = user.name
    password = user.password
    email = user.email
    birthday = user.birthday
    if username == "" or password == "" or email == "" or birthday == "" or name == "":
        return False
    return True


def validate_email(email: str):
    pattern: str = r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.fullmatch(pattern, email)


def validate_birthday(birthday: str):
    pattern: str = r"\d{4}-\d{2}-\d{2}"
    return re.fullmatch(pattern, birthday)



