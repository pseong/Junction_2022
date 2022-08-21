from typing import List

from fastapi import Depends, HTTPException, status, WebSocket
from jose import JWTError, jwt
from fastapi.security import OAuth2AuthorizationCodeBearer

from sqlalchemy.orm import Session

import schemas
from database import SessionLocal
from models import User
from SETTING import SECRET_KEY, ALGORITHM
from services import get_user


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Node:
    def __init__(self):
        self.id = "0"
        self.type = "rootNode"
        self.data = {
            "label": "play",
            "id": 0,
            "childs": [],
            "parent": -1,
            "color": "#FFFFFF"
        }
        self.position =  {"x": 0, "y": 0}
        self.up = 0
        self.down = 0


class Factory:
    def __init__(self):
        self.nextIdx = 1
        self.nodes = {"0": Node()}
        self.edges = []

    def create(self, parent: int, label: str, color: str):
        node = Node()
        node.id = str(self.nextIdx)
        node.data["label"] = label
        node.data["id"] = self.nextIdx
        node.data["parent"] = parent
        node.data["color"] = color
        node.type = "myNode"
        self.nodes[str(node.id)] = node
        self.nodes[str(parent)].data["childs"].append(self.nextIdx)
        self.nodes[str(node.id)].position['x'] += self.nodes[str(parent)].position['x'] + 350
        self.nodes[str(node.id)].position['y'] += self.nodes[str(parent)].position['y'] + (len(self.nodes[str(parent)].data['childs']) - 1) * 200
        self.edges.append({
            "id": f"e{parent}-{self.nextIdx}",
            "source": str(parent),
            "target": str(self.nextIdx),
            "style": {
                "stroke": "#6D7A79",
                "stroke-width": 4
            }
        })
        self.nextIdx = self.nextIdx + 1
        self.h = 0

    def createDfs(self, id: int, lv: int):
        for child in self.nodes[str(id)].data['childs']:
            self.createDfs(child, lv + 1)
        self.nodes[str(id)].data['x'] = lv * 200
        self.nodes[str(id)].data['y'] = self.h * 100
        self.h = self.h + 1

    def update(self, id: int, label: str, color: str, x: int, y: int):
        print(label, color)
        if label: self.nodes[str(id)].data["label"] = label
        if color: self.nodes[str(id)].data["color"] = color
        if x: self.nodes[str(id)].position['x'] = x
        if y: self.nodes[str(id)].position['y'] = y

    def remove(self, id: int):
        node = self.nodes[str(id)]
        self.removeDfs(node)

    def removeDfs(self, node: Node):
        while node.data["childs"]:
            self.removeDfs(self.nodes[str(node.data["childs"][0])])
        self.nodes[str(self.nodes[str(node.id)].data["parent"])].data["childs"].remove(int(node.id))
        del self.nodes[str(node.id)]



factory = Factory()

def get_factory():
    return factory

oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl="token", authorizationUrl="authorization")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    user = get_user(db, token_data.id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def update(self):
        for connection in self.active_connections:
            try:
                ret = {'code': 1, 'nodes': [], 'edges': []}
                for id in factory.nodes:
                    ret['nodes'].append(factory.nodes[id].__dict__)
                ret['edges'] = factory.edges
                await connection.send_json(ret)
            except:
                pass

manager = ConnectionManager()

def get_connection():
    return manager