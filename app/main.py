from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app import models  # noqa: F401 — registers models with SQLModel.metadata
from app.routers import auth, announcements

# API metadata shown in the Swagger UI and OpenAPI schema.
tags_metadata = [
    {"name": "Auth", "description": "Registration and login."},
    {"name": "Announcements", "description": "Create, read and delete campus announcements."},
]

# Create the FastAPI application instance and configure the public API metadata.
app = FastAPI(
    title="Student Hub API",
    description="Backend for the Student Hub, a student companion app covering academic, admin and social needs.",
    version="0.1.0",
    openapi_tags=tags_metadata,
)

# Ensure all SQLModel tables exist before the app serves requests.
SQLModel.metadata.create_all(engine)

# Register endpoint groups for authentication and announcements.
app.include_router(auth.router)
app.include_router(announcements.router)
