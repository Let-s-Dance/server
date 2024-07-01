from typing import List

from .database import Base
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username = Column(String, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    authority = Column(String, nullable=False)

    recent_videos: Mapped[List["RecentVideo"]] = relationship()
    user_upload_videos: Mapped[List["UserUploadVideo"]] = relationship()


class MusicVideo(Base):
    __tablename__ = 'music_video'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    musician: Mapped[str] = mapped_column(nullable=False)
    file_location: Mapped[str] = mapped_column(nullable=False)
    thumbnail_location: Mapped[str] = mapped_column(nullable=False)

    recent_videos: Mapped[List["RecentVideo"]] = relationship()
    user_upload_videos: Mapped[List["UserUploadVideo"]] = relationship()


class RecentVideo(Base):
    __tablename__ = 'recent_video'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    mv_id: Mapped[int] = mapped_column(ForeignKey('music_video.id'))
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    thumbnail_endpoint: Mapped[str] = mapped_column(nullable=False)

class UserUploadVideo(Base):
    __tablename__ = 'user_upload_video'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    file_location: Mapped[str] = mapped_column(nullable=False)
    mv_id: Mapped[int] = mapped_column(ForeignKey('music_video.id'))
    score: Mapped[float] = mapped_column(nullable=False)
