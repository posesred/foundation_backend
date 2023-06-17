from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from blog.hashing import Hash
from blog.model import User
from blog.schema import UserResponse


def create_user(request: User) -> UserResponse:
    """
    Creates a user
    :param request:
    :return: UserResponse
    """
    # due to the new changes, this will save him automatically
    new_user = User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    return UserResponse(name=new_user.name, email=new_user.email, blogs=[])


def get_user(user_id: int):
    """
    Gets a user by id
    :param user_id:
    :return: UserResponse
    """
    if user := User.session.query(User).filter_by(id=user_id).first():
        return UserResponse(name=user.name, email=user.email, blogs=[])

    # its ok to return nothing, this will fail a null check and allow us to know the status
    # these exceptions should be handled in the router

    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")


def get_all_users() -> List[UserResponse]:
    """
    Gets all users
    :return:  List[UserResponse]
    """
    return User.session.query(User).all()