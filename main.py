from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

import service, models, schemas
from database import SessionLocal, engine

import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return service.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = service.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return service.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = service.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/auth/")
def auth(request: Request, db: Session = Depends(get_db)):
    if "Authorization" in request.headers:
        token = request.headers["Authorization"]
    else:
        raise HTTPException(status_code=404, detail="not found Authorization in headers")
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="failed to asignin")

    user_json = response.json()
    item = schemas.UserCreate
    item.sub = user_json['sub']
    item.email = user_json['email']
    item.first_name = user_json['given_name']
    item.last_name = user_json['family_name']
    item.name = user_json['name']
    user = service.user_get_or_create(db, item)

    # token = login(user=user)
    # return {"token": token}