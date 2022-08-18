from fastapi import FastAPI

import SETTING
SETTING.init()

from routers import login, user, item
from database import Base, engine

def include_router(app):
    app.include_router(login.router, prefix='/login')
    app.include_router(user.router, prefix='/users')
    app.include_router(item.router, prefix='/items')

def start_application():
    app = FastAPI()
    include_router(app)
    Base.metadata.create_all(bind=engine)
    return app

app = start_application()