from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    is_private: bool = False
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime


class PostIn(BaseModel):
    title: str
    description: str
    is_private: bool = False
