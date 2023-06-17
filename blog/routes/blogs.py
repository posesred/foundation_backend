from fastapi import status
from starlette.requests import Request

from . import router
from blog.model import Blog
from blog.schema import BlogResponse, BlogResponseDetails


@router.post("/", response_model=BlogResponseDetails, tags=["blog"],  status_code=status.HTTP_201_CREATED)
def create(blog: BlogResponse, request: Request):
    """
    Creates a blog
    :param blog:
    :param request:
    :return:    BlogResponseDetails
    """
    # we would get current user from request with a middleware:
    user = request.user  # <--- this uses Starlette auth middleware to get user session

    blog = Blog(**blog.dict(), user_id=user.id)  # <--- this works because of our mixin
    return BlogResponseDetails.from_orm(blog)  # <--- this serializes the response from orm to pydantic
