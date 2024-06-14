from pydantic import BaseModel
from datetime import date, datetime
from fastapi import UploadFile


## recent music

class RecentMusicCreate(BaseModel):
    user_id: int
    music_id: int
    add_date: str


class RecentMusic(BaseModel):
    id: int
    user_id: int
    music_id: int
    add_date: date

    class Config:
        from_attributes = True


## user schemas

class UserCreate(BaseModel):
    user_real_name: str
    user_name: str
    password: str
    email: str
    birthday: str


class UserUpdate(BaseModel):
    user_real_name: str
    email: str


class User(BaseModel):
    id: int
    user_name: str
    email: str

    recent_musics: list[RecentMusic] = []

    class Config:
        from_attributes = True


## music schemas

class MusicCreateDto(BaseModel):
    name: str
    musician: str
    file: UploadFile


class MusicCreate(BaseModel):
    name: str
    musician: str
    file_location: str


class MusicUpdate(MusicCreate):
    pass


class Music(BaseModel):
    id: int
    name: str
    musician: str
    file_location: str
    recent_musics: list[RecentMusic] = []

    class Config:
        from_attributes = True


## login  schemas

class UserLogin(BaseModel):
    user_name: str
    password: str


## session

class SessionData(BaseModel):
    user_id: int
    time: datetime
