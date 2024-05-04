import datetime

from pydantic import BaseModel

from database.schemas.utils import PeeweeGetterDict


class CommentCreate(BaseModel):
    text: str


class Comment(BaseModel):
    id: int
    user_id: int
    project_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict