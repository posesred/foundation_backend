

from fastapi import FastAPI


from blog import model
from blog.database import engine
from blog.router import blogs, users , auth

app = FastAPI(
    tags=['Authentication']
)

model.Base.metadata.create_all(bind = engine)


app.include_router(auth.router)
app.include_router(blogs.router)
app.include_router(users.router)




