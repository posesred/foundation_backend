from blog.database import Base
from sqlalchemy import Column, INTEGER, String

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(INTEGER,primary_key=True, index=True)
    title = Column(String)
    body = Column(String)