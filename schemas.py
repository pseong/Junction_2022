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


class Word(BaseModel):
    word: str


class CreateNode(BaseModel):
    parent: int
    label: str
    color: str


class UpdateNode(BaseModel):
    id: int
    label: Union[str, None]
    color: Union[str, None]
    x: Union[int, None]
    y: Union[int, None]


class RemoveNode(BaseModel):
    id: int