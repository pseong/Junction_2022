from typing import List

from fastapi import Depends, HTTPException, APIRouter, WebSocket
from sqlalchemy.orm import Session

import schemas
from dependencies import Factory, get_factory, ConnectionManager, get_connection
router = APIRouter()

@router.post("/create", name = '노드 생성', tags=['노드'])
async def createNode(item: schemas.CreateNode, factory: Factory = Depends(get_factory), manager: ConnectionManager = Depends(get_connection)):
    factory.create(item.parent, item.label, item.color)
    await manager.update()

@router.post("/update", name = '노드 수정', tags=['노드'])
async def updateNode(item: schemas.UpdateNode, factory: Factory = Depends(get_factory), manager: ConnectionManager = Depends(get_connection)):
    factory.update(item.id, item.label, item.color, item.x, item.y)
    await manager.update()

@router.post("/remove", name = '노드 제거', tags=['노드'])
async def removeNode(item: schemas.RemoveNode, factory: Factory = Depends(get_factory), manager: ConnectionManager = Depends(get_connection)):
    factory.remove(item.id)
    await manager.update()