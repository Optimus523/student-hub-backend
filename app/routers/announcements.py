from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlmodel import Session, select

from app.database import get_db
from app.models import Announcement
from app.schemas.announcement import AnnouncementIn

router = APIRouter(tags=["Announcements"])


@router.post("/announcements/")
def create_announcement(data: AnnouncementIn, db: Session = Depends(get_db)):
    announcement = Announcement(**data.model_dump())
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    return announcement


@router.get("/announcements/")
def list_announcements(db: Session = Depends(get_db)):
    return db.exec(select(Announcement)).all()


@router.get("/announcements/{id}")
def get_announcement(id: Annotated[int, Path(ge=1)], db: Session = Depends(get_db)):
    announcement = db.get(Announcement, id)
    if announcement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Announcement with id {id} does not exist",
        )
    return announcement


@router.delete("/announcements/{id}")
def delete_announcement(id: Annotated[int, Path(ge=1)], db: Session = Depends(get_db)):
    announcement = db.get(Announcement, id)
    if announcement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Announcement with id {id} does not exist",
        )
    db.delete(announcement)
    db.commit()
    return {"message": "Announcement deleted successfully"}
