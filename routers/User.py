from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .. import schema, database, models

router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={
        404: {"user": "User is not authenticated"}
    }
)

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(pwd: str):
    return pwd_ctx.hash(pwd)


@router.get("/", response_model=List[schema.UserResponse])
def get_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).filter(models.User.id == id).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user: schema.User, db: Session = Depends(database.get_db)):
    new_user = models.User()
    new_user.name = user.name
    new_user.email = user.email
    new_user.password = hash_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=schema.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"User with id {user_id} not found"}
        )
    return user
