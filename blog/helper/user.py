from .. import schema, model
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..hashing import Hash


def create_user(response: schema.UserResponse,db: Session ):
    new_user = model.User(name=response.name, email=response.email, password=Hash.bcrypt(response.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(id: int, db: Session):
    if user := db.query(model.User).filter(model.User.id == id).first():
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")