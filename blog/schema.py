from typing import Any, List, Optional

from pydantic import BaseModel


class BlogBase(BaseModel):
    class Config():
        orm_mode = True


class BlogResponse(BlogBase):
    title:str
    body: str


class User(BaseModel):
    name:str
    email: str
    password:str

class UserLogin(BaseModel):
    email: str
    password: str

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

class BaseResponse(BaseModel):
    success: bool = False
    error: Optional[str] = None
    response: Optional[Any] = None

class TokenResponse(BaseResponse):
    response = Optional[Token]


class TokenData(BaseModel):
    email: str | None = None


class GetBlogsResponse(BaseResponse):
    response: BlogResponseDetails | None

