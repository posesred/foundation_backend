from pydantic import BaseConfig
from sqlalchemy.orm import relationship

from blog.database import Base, ModelMixin
from sqlalchemy import Column, INTEGER, Integer, String, ForeignKey, Text


class Blog(ModelMixin):
    __tablename__ = 'blogs'
    id = Column(INTEGER,primary_key=True, index=True)
    title = Column(String(40))
    body = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="blogs")

    class Config(BaseConfig):
        orm_mode = True

class User(ModelMixin):
    __tablename__ = 'users'
    id = Column(INTEGER,primary_key=True, index=True)
    name = Column(String(40)) # if your going to use string, limit the size otherwise use Text
    email = Column(String(120))
    password = Column(String(120))

    blogs = relationship("Blog", back_populates="creator")