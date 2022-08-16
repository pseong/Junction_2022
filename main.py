from fastapi import FastAPI

from routers import login, user, item
from database import Base

from database import engine

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