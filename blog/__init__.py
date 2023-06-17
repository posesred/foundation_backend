from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from blog.oauth2 import oauth2_scheme
from blog.routes import router


app = FastAPI()
# init app tools here

SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})
_Session: sessionmaker = sessionmaker(bind=engine, autocommit = False, autoflush= False )


app.include_router(router, prefix="/blog", tags=["blog"], dependencies=[Depends(oauth2_scheme)])