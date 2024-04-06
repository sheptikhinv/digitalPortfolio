from typing import Optional

import pydantic
from pydantic import BaseModel

from database.schemas.utils import PeeweeGetterDict


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    education: Optional[str] = None
    description: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[pydantic.EmailStr] = None


class ProfileCreate(ProfileUpdate):
    name: str


class Profile(ProfileUpdate):
    user_id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ProfileResponse(BaseModel):
    can_edit: bool
    data: Optional[Profile] = None
