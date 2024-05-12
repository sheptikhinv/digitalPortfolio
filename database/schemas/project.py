from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from database.schemas.utils import PeeweeGetterDict


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ProjectCreate(BaseModel):
    title: str
    description: str


class Project(ProjectCreate):
    id: int
    user_id: int
    username: str
    likes_count: int
    comments_count: int
    created_at: datetime

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ProjectOutput(BaseModel):
    can_edit: bool
    is_liked: bool
    data: Optional[Project] = None
