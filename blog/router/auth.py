from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from blog import schema, database, model
from blog.hashing import Hash

router = APIRouter()


@router.post("/login")
def login(response: schema.Login, db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.email == response.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not Hash.verify(user.password, response.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")
    # generate a jwt token and return
    return user