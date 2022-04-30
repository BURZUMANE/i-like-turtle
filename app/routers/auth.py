from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models
from ..oauth2 import create_access_token
from ..utils import verify_password

router = APIRouter(tags=['authentication'])


@router.post('/login', response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    print(user_credentials)
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_NOT_FOUND, detail=f'invalid credentials')

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_NOT_FOUND, detail=f'invalid credentials')

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
