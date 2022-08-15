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
    first_name: str
    last_name: str
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True