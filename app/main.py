from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500",], #"http://10.207.238.74:5000"],
    allow_origin_regex=r"http://(10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+):\d+",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Ensure all SQLModel tables exist before the app serves requests.
SQLModel.metadata.create_all(engine)

# Register endpoint groups for authentication and announcements.
app.include_router(auth.router)
app.include_router(announcements.router)
