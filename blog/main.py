from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from blog import model
from blog.database import engine, SessionLocal
from blog.schema import Blog

app = FastAPI()

model.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog")
def create(blog:Blog, db: Session = Depends(get_db)):
    new_blog = model.Blog(title = blog.title, body = blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog")
def all(db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all()
    return blogs
