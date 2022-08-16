
from typing import Union
from datetime import datetime, timedelta

from jose import jwt

from sqlalchemy.orm import Session

import schemas, SETTING
from models import User, Item


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_sub(db: Session, sub: str):
    return db.query(User).filter(User.sub == sub).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(sub=user.sub, email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def user_get_or_create(db: Session, user: schemas.UserCreate):
    user_db = get_user_by_sub(db, user.sub)
    if user_db:
        return user_db
    else:
        return create_user(db, user)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SETTING.SECRET_KEY, algorithm=SETTING.ALGORITHM)
    return encoded_jwt