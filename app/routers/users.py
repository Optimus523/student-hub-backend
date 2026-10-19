import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlmodel import Session, select

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserUpdate
from app.security import get_current_user, hash_password, verify_password

router = APIRouter(tags=["Users"])

UPLOAD_DIR = Path("uploads/avatars")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE = 2 * 1024 * 1024  # 2 MB


@router.get("/users/me")
def get_me(user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return {
        "id": user.id,
        "username": user.username,
        "avatar_url": user.avatar_url,
    }


@router.patch("/users/me")
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Update the current user's username and/or password."""
    changed = False

    if data.username is not None and data.username != user.username:
        existing = db.exec(select(User).where(User.username == data.username)).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken",
            )
        user.username = data.username
        changed = True

    if data.new_password is not None:
        if not data.current_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="current_password is required to change password",
            )
        if not verify_password(data.current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect",
            )
        user.hashed_password = hash_password(data.new_password)
        changed = True

    if not changed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nothing to update",
        )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "username": user.username,
        "avatar_url": user.avatar_url,
    }


@router.post("/users/me/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Upload or replace the current user's profile picture."""
    # 1. Validate content type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, or WebP images are allowed",
        )

    # 2. Read file into memory and check size
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large (max 2 MB)",
        )

    # 3. Delete old avatar if one exists
    if user.avatar_url:
        old_path = Path("uploads") / user.avatar_url.replace("/uploads/", "")
        if old_path.exists():
            old_path.unlink()

    # 4. Save new file with unique name
    ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}[file.content_type]
    filename = f"user_{user.id}_{uuid.uuid4().hex[:8]}{ext}"
    file_path = UPLOAD_DIR / filename
    with open(file_path, "wb") as f:
        f.write(contents)

    # 5. Update DB with the public URL
    user.avatar_url = f"/uploads/avatars/{filename}"
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "username": user.username,
        "avatar_url": user.avatar_url,
    }