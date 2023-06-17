from blog.model import User
from blog.schema import UserResponse
from blog.helper import user_adapter
from . import router


@router.post("/", response_model=UserResponse, tags=["auth"], status_code=201)
def create_user(response: User):
    """
    Creates a user
    :param response:
    :return: UserResponse
    """
    # we use this instead of the method in blog because more needs to be done for this session,
    # like hashing the password and any other user specific logic (like adding a blog?)
    # adapters like this are good when needed, and pointless when not
    return user_adapter.create_user(response)
