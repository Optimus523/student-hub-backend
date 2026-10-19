from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlmodel import Session, select

from app.database import get_db
from app.models.assignment import Assignment
from app.models.user import User
from app.schemas.assignment import AssignmentIn
from app.security import get_current_user

router = APIRouter(tags=["Assignments"])


@router.post("/assignments/")
def create_assignment(
    data: AssignmentIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Create a new assignment. The author is derived from the JWT token."""
    # Notice: author_id comes from `user.id`, NOT from `data`. 
    # This prevents impersonation (as we discussed in the schema step).
    assignment = Assignment(**data.model_dump(), author_id=user.id)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@router.get("/assignments/")
def list_assignments(db: Session = Depends(get_db)):
    """Return all assignments, sorted by due date (soonest first)."""
    # We join with User to get the author's username, just like announcements.
    # We order by due_date ascending so the most urgent assignments appear first.
    # The secondary sort by id ensures deterministic order if two share a due date.
    statement = (
        select(Assignment, User.username)
        .join(User, Assignment.author_id == User.id)
        .order_by(Assignment.due_date, Assignment.id)
    )
    
    results = db.exec(statement).all()
    
    # Format the response to include the joined username
    return [
        {
            "id": a.id,
            "title": a.title,
            "description": a.description,
            "course_code": a.course_code,
            "due_date": a.due_date,
            "author_id": a.author_id,
            "author_username": username,
            "created_at": a.created_at,
        }
        for a, username in results
    ]


@router.get("/assignments/{id}")
def get_assignment(
    id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
):
    """Fetch a single assignment by ID."""
    assignment = db.get(Assignment, id)
    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment with id {id} does not exist",
        )
    return assignment


@router.delete("/assignments/{id}")
def delete_assignment(
    id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Delete an assignment. Only the original author can do this."""
    assignment = db.get(Assignment, id)
    
    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment with id {id} does not exist",
        )
        
    # Security check: ensure the person deleting is the one who created it.
    # Without this, any logged-in user could delete anyone's assignment.
    if assignment.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own assignments",
        )
        
    db.delete(assignment)
    db.commit()
    return {"message": "Assignment deleted successfully"}