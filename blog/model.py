from sqlalchemy.orm import relationship

from blog.database import Base
from sqlalchemy import Column, INTEGER, String, ForeignKey


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(INTEGER,primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(INTEGER,ForeignKey("users.id"))

    creator = relationship("User", back_populates="blogs")

class User(Base):
    __tablename__ = 'users'
    id = Column(INTEGER,primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("Blog", back_populates="creator")