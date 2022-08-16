from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import schemas
from dependencies import get_db, get_current_active_user
from services import create_user_item, get_items
from models import User

router = APIRouter()

@router.post("/users/items", name = '개인 아이템 생성', tags=['아이템'],
            description='생성된 아이템 반환', response_model=schemas.Item)
def create_item_for_user(item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_user_item(db=db, item=item, user_id=current_user.id)


@router.get("/items", name = '모든 아이템', tags=['아이템'],
            description='모든 아이템 반환', response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    items = get_items(db, skip=skip, limit=limit)
    return items