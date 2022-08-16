from typing import List, Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    sub: str
    email: str
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Union[str, None] = None