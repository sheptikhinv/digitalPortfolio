import pydantic
from pydantic import BaseModel

from database.schemas.utils import PeeweeGetterDict


class UserBase(BaseModel):
    email: pydantic.EmailStr


class UserInput(UserBase):
    password: str


class UserOutput(UserBase):
    id: int


class User(UserBase):
    id: int
    password: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class Token(BaseModel):
    access_token: str
    token_type: str

