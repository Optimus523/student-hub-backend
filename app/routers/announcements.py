from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlmodel import Session, select

from app.database import get_db
from app.models import Announcement
from app.schemas.announcement import AnnouncementIn
from app.security import get_current_user
from app.models import User

# Register these endpoints under the "Announcements" OpenAPI group.
router = APIRouter(tags=["Announcements"])


@router.post("/announcements/")
def create_announcement(data: AnnouncementIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Create a new announcement and associate it with the authenticated user."""
    # Attach the logged-in user as the author before saving the record.
    announcement = Announcement(**data.model_dump(), author_id=user.id)
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    return announcement


@router.get("/announcements/")
def list_announcements(db: Session = Depends(get_db)):
    """Return all stored announcements, including the author's username."""
    # Join the Announcement table with the User table to get the username
    statement = select(Announcement, User.username).join(User, Announcement.author_id == User.id)
    results = db.exec(statement).all()
    
    # Format it into a clean list of dictionaries
    return [
        {
            "id": ann.id,
            "title": ann.title,
            "body": ann.body,
            "author_id": ann.author_id,
            "author_username": username,  # <-- New!
            "created_at": ann.created_at, # <-- New!
        }
        for ann, username in results
    ]


@router.get("/announcements/{id}")
def get_announcement(id: Annotated[int, Path(ge=1)], db: Session = Depends(get_db)):
    """Fetch a single announcement by its numeric ID."""
    announcement = db.get(Announcement, id)
    if announcement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Announcement with id {id} does not exist",
        )
    return announcement


@router.delete("/announcements/{id}")
def delete_announcement(id: Annotated[int, Path(ge=1)], db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Delete an announcement if it exists and the caller is authenticated."""
    announcement = db.get(Announcement, id)
    if announcement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Announcement with id {id} does not exist",
        )

    # Remove the announcement record from the database.
    db.delete(announcement)
    db.commit()
    return {"message": "Announcement deleted successfully"}
