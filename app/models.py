from .database import Base
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_real_name = Column(String, nullable=False)
    user_name = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)

    recent_musics: Mapped["RecentMusic"] = relationship()


class Music(Base):
    __tablename__ = 'musics'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    musician: Mapped[str] = mapped_column(nullable=False)
    file_location: Mapped[str] = mapped_column(nullable=False)
    recent_musics: Mapped["RecentMusic"] = relationship()


class RecentMusic(Base):
    __tablename__ = 'recent_music'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    music_id: Mapped[int] = mapped_column(ForeignKey("musics.id"))
    add_date = Column(Date, nullable=False)
