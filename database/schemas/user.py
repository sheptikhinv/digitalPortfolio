import pydantic
from pydantic import BaseModel

from database.schemas.utils import PeeweeGetterDict


class UserBase(BaseModel):
    email: pydantic.EmailStr
    password: str


class UserCreate(UserBase):
    ...


class UserAuthenticate(UserBase):
    ...


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class Token(BaseModel):
    access_token: str
    token_type: str

