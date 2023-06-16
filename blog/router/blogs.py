from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from blog import model, schema, oauth2
from blog.database import get_db
from blog.helper import blog as helper
from blog.schema import BlogResponse

router = APIRouter(
    tags=['blogs'],
    prefix="/blog"
)
@router.post("/",)
def create(blog:BlogResponse, db: Session = Depends(get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    return helper.create(blog, db)

@router.get("/", response_model= List[schema.BlogResponseDetails])
def all(db: Session = Depends(get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    return helper.get_all(db)

@router.get("/{id}", response_model= schema.BlogResponseDetails)
def show(id: int, db: Session = Depends(get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    return helper.get_first(id,db)
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    return helper.destroy(id, db)



@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, response: schema.BlogResponse, db:Session = Depends(get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    return helper.update(id ,response, db)