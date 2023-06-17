from datetime import datetime, timedelta, timezone

from jwt import PyJWT

from settings import Config


jwt = PyJWT()

from blog.schema import Token, TokenData

SECRET_KEY = Config.jwt_secret
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user_claim_base: str, expires_delta: timedelta | None = None) -> Token:
    """
    Creates a JWT token
    :param user_claim_base:
    :param expires_delta:
    :return: Token
    """
    user_claim = dict(
        sub=user_claim_base,
        iat=datetime.now(timezone.utc),
        exp=datetime.now(timezone.utc)
        + expires_delta or timedelta(minutes=15)
    )
    token = jwt.encode(user_claim, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=token, token_type="bearer")

class CredentialsException(Exception):
    """
    Exception for credentials
    """
    def __init__(self, message: str = "Could not validate credentials"):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


def verify_token(token: str) -> TokenData:
    """
    Verifies the JW token
    :param token
    :return: TokenData
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise
        return TokenData(email=email)
    except JWTError as e:
        # should actually be an http error
        raise CredentialsException from e

#