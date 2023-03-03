from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schema, database, models, HashingUtil
from ..token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/token", response_model=schema.Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Invalid Credential"}
        )

    if HashingUtil.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Wrong Password"}
        )
    # now generate token and return `
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
