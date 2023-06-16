from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from blog import model, schema
from blog.database import get_db
from blog.schema import UserResponse
from blog.helper import user as helper

router = APIRouter(
    prefix="/user",
    tags=['users']
)


@router.post("/", response_model= UserResponse)
def create_user(response: schema.User,db:Session = Depends(get_db)):
    return helper.create_user(response,db)

#
@router.get("/{id}", response_model= UserResponse)
def get_user(id: int , db:Session = Depends(get_db)):
    return helper.get_user(id,db)


@router.get("/")
def get_all_users(db:Session = Depends(get_db)):
    return helper.get_all_users(db)