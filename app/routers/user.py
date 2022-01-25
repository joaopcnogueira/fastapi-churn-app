from fastapi import APIRouter, status, Depends
from app import models, schemas, utils
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List


router = APIRouter(
    prefix="/users",
    tags=["user"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    user = db.query(models.User).all()

    return user