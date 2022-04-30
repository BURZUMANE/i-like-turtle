from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from ..utils import get_password_hash
from .. import models, schemas

router = APIRouter(
    prefix='/users',
    tags=['users']
)


# ============== users ==============

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.dict()['password'])
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{user_id}', response_model=schemas.UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return user
