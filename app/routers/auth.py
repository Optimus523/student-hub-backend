from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database import get_db
from app.models import User
from app.schemas.user import UserCreate, UserPublic
from app.security import hash_password, verify_password

router = APIRouter(tags=["Auth"])


@router.post("/users/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.exec(select(User).where(User.username == data.username)).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username {data.username} already exists",
        )
    user = User(hashed_password=hash_password(data.password), username=data.username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login/")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = db.exec(select(User).where(User.username == form_data.username.lower())).first()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "login OK"}
