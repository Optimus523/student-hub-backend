import os
from security import hash_password, verify_password
from dotenv import load_dotenv
from fastapi import FastAPI, Path, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, StringConstraints
from typing import Annotated
from sqlmodel import Field, Session, select, SQLModel, create_engine


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


tags_metadata = [
    {"name": "Auth", "description": "Registration and login."},
    {"name": "Announcements", "description": "Create, read and delete campus announcements."},
]

app = FastAPI(    title="Student Hub API",
    description="Backend for the Student Hub, a student companion app covering academic, admin and social needs. Built with FastAPI and PostgreSQL.",
    version="0.1.0",
    openapi_tags=tags_metadata)


class AnnouncementIn(BaseModel):
    title: str
    body: str

class Announcement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    body: str

class User(SQLModel, table=True):
        __tablename__ = "users"
        id : int | None = Field(default=None, primary_key=True)
        username: str = Field(unique=True, index=True)
        hashed_password: str

class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=30, pattern=r"^[A-Za-z0-9_]+$", to_lower=True)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=128)]

class UserPublic(BaseModel):
    id : int
    username: str

SQLModel.metadata.create_all(engine)

announcements = []

@app.post("/users/", response_model=UserPublic, status_code=status.HTTP_201_CREATED, tags=["Auth"])
def register(data: UserCreate):
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == data.username)).first()
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Username {data.username} already exists")
        user = User(hashed_password=hash_password(data.password), username=data.username)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@app.post("/login/", tags=["Auth"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == form_data.username.lower())).first()
        if user is None or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},)
        return {"message" : "login OK"}


@app.post("/announcements/", tags=["Announcements"])
def create_announcement(data: AnnouncementIn):
    announcement = Announcement(**data.model_dump())
    with Session(engine) as session:
        session.add(announcement)
        session.commit()
        session.refresh(announcement)
        return announcement

@app.get("/announcements/", tags=["Announcements"])
def list_announcements():
    with Session(engine) as session:
        announcements = session.exec(select(Announcement)).all()
        return announcements

@app.get("/announcements/{id}", tags=["Announcements"])
def get_announcement(id: Annotated[int, Path(ge=1)]):
    with Session(engine) as session:
        announcement = session.get(Announcement, id)
        if announcement is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Announcement with id {id} does not exist")
        return announcement

@app.delete("/announcements/{id}", tags=["Announcements"])
def delete_announcement(id: Annotated[int, Path(ge=1)]):
    with Session(engine) as session:
            announcement = session.get(Announcement, id)
            if announcement is None:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Announcement with id {id} does not exist")
            session.delete(announcement)
            session.commit()
            return {"message" : "Announcement deleted successfully"}
