from pydantic import BaseModel
from datetime import datetime


class SessionData(BaseModel):
    id: int
    created_at: datetime
    authority: str
