from pydantic import BaseModel
from datetime import datetime


# Pydantic schema for Session (excluding methods)
class SessionSchema(BaseModel):
    id: int
    session_token: str
    user_id: int
    expires_at: datetime

    class Config:
        orm_mode = True
