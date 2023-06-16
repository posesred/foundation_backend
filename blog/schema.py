from typing import List

from pydantic import BaseModel


class BlogResponse(BaseModel):
    title:str
    body: str

class BlogBase(BlogResponse):
    class Config():
        orm_mode = True


class User(BaseModel):
    name:str
    email: str
    password:str


class UserResponse(BaseModel):
    name: str
    email: str
    blogs: List[BlogBase] = []
    class Config():
        orm_mode = True


class BlogResponseDetails(BaseModel):
    title: str
    body: str
    creator: UserResponse
    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None