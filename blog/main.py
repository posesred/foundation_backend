from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from blog import model, schema
from blog.database import engine, SessionLocal
from blog.hashing import Hash
from blog.schema import BlogResponse, UserResponse
from passlib.context import CryptContext
app = FastAPI()

model.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", tags=['blogs'])
def create(blog:BlogResponse, db: Session = Depends(get_db)):
    new_blog = model.Blog(title = blog.title, body = blog.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog", response_model= List[schema.BlogResponseDetails], tags=['blogs'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all()
    return blogs

@app.get("/blog/{id}", response_model= schema.BlogResponseDetails, tags=['blogs'])
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    return blog

@app.delete("/blog/{id}", status_code= status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"Deleted": "Successfully"}

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id: int, response: schema.BlogResponse, db:Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    blog.update({"title": response.title, "body": response.body}, synchronize_session=False)
    db.commit()
    return{"Updated": "Successfully"}


@app.post("/user", response_model= UserResponse, tags=['users'])
def create_user(request: schema.User,db:Session = Depends(get_db)):
    new_user = model.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", response_model= UserResponse, tags=['users'])
def get_user(id: int , db:Session = Depends(get_db)):
    if user := db.query(model.User).filter(model.User.id == id).first():
        return user
    else:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")