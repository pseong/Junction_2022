from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import schemas
from services import get_users, get_user
from dependencies import get_db, get_current_active_user
from models import User


router = APIRouter()


@router.get("/me", name = '개인 정보', tags=['개인 정보'], # /{user_id} 보다 위에 있어야 함
            description='접근 토큰의 사용자 정보 반환', response_model=schemas.User)
async def read_users_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/", name = '모든 사용자 정보', tags=['개인 정보'],
            description='모든 사용자 정보를 반환', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", name = '사용자 정보', tags=['개인 정보'],
            description='"id"에 해당하는 사용자 정보 반환', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user