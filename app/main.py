from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app import models  # noqa: F401 — registers models with SQLModel.metadata
from app.routers import auth, announcements

tags_metadata = [
    {"name": "Auth", "description": "Registration and login."},
    {"name": "Announcements", "description": "Create, read and delete campus announcements."},
]

app = FastAPI(
    title="Student Hub API",
    description="Backend for the Student Hub, a student companion app covering academic, admin and social needs.",
    version="0.1.0",
    openapi_tags=tags_metadata,
)

SQLModel.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(announcements.router)
