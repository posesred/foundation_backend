from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .. import model , schema



def get_all(db: Session):
    blogs = db.query(model.Blog).all()
    return blogs

def create(blog: schema.BlogResponse, db: Session):
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

def destroy(id: int, db: Session):
    blog = db.query(model.Blog).filter(model.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"Deleted": "Successfully"}

def update(id: int, response: schema.BlogResponse,db: Session):
    blog = db.query(model.Blog).filter(model.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    blog.update({"title": response.title, "body": response.body}, synchronize_session=False)
    db.commit()
    return {"Updated": "Successfully"}

def get_first(id: int, db:Session):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    return blog
