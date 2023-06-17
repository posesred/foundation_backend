from fastapi import status

from blog.hashing import Hash
from blog.model import User
from blog.schema import BaseResponse, Token, TokenResponse, UserLogin
from blog.token import create_access_token
from blog.routes import router


@router.post("/login", response_model=TokenResponse, tags=['Authentication'], status_code=status.HTTP_200_OK)
def login(context: UserLogin):
    """
    Logs a user in
    :param context:
    :return:
    """
    user = User.session.query(User).filter_by(email=context.email).first()
    verified = Hash.verify(user.password, context.password)
    if not verified:
        return BaseResponse(response="Invalid Credentials")

    # seriously that shit sucks, stop it
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
    #     )
    # if not Hash.verify(user.password, response.password):
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password"
    #     )
    # generate a jwt token and return
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # if were using full rest its ok to use 404, etc but the truth is that really sucks, why would we 404

    access_token: Token = create_access_token(user.email)
    return TokenResponse(success=True, response=access_token)