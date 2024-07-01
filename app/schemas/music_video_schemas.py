from pydantic import BaseModel
from .recent_video_schemas import RecentVideo


class MusicVideoCreateRequest(BaseModel):
    title: str
    musician: str

    recent_videos: list[RecentVideo] = []

    class Config:
        from_attributes = True
