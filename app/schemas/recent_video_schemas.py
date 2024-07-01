from pydantic import BaseModel
from datetime import datetime


class RecentVideo(BaseModel):
    id: int
    created_at: datetime

    user_id: int
    mv_id: int
    thumbnail_endpoint: str

    class Config:
        from_attributes = True

