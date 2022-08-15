from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import SETTING

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{SETTING.USER}:{SETTING.PASSWORD}@{SETTING.HOST}:{SETTING.PORT}/{SETTING.DATABASE}?charset-utf8"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()