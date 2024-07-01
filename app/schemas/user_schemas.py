from pydantic import BaseModel
from .recent_video_schemas import RecentVideo


class UserCreateRequest(BaseModel):
    username: str
    password: str
    name: str
    email: str
    birthday: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    username: str
    authority: str
    hashed_password: str


class UserResponseWithRecentVideo(BaseModel):
    id: int
    username: str
    authority: str

    recent_videos: list[RecentVideo]
