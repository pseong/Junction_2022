from datetime import timedelta
from typing import List

from fastapi import Depends, WebSocketDisconnect, WebSocket, APIRouter
from sqlalchemy.orm import Session

import schemas
from dependencies import Factory, get_db, get_connection, ConnectionManager, get_factory
from services import user_get_or_create, create_access_token
from SETTING import ACCESS_TOKEN_EXPIRE_MINUTES

import requests

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(f"client connected : {websocket.client}")
    await websocket.accept() # client의 websocket접속 허용
    await websocket.send_text(f"Welcome client : {websocket.client}")
    while True:
        data = await websocket.receive_text()  # client 메시지 수신대기
        print(f"message received : {data} from : {websocket.client}")
        await websocket.send_text(f"Message text was: {data}") # client에 메시지 전달


@router.websocket("/connect/{client_id}")
async def connect(websocket: WebSocket, client_id: str, manager: ConnectionManager = Depends(get_connection), factory: Factory = Depends(get_factory)):
    await manager.connect(websocket)
    try:
        ret = {'nodes': [], 'edges': []}
        for id in factory.nodes:
            ret['nodes'].append(factory.nodes[id].__dict__)
        ret['edges'] = factory.edges
        await websocket.send_json(ret)
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client #{client_id} left the chat")
    except:
        manager.disconnect(websocket)
