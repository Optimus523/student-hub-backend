from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class Assignment(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    course_code: str
    due_date: datetime
    author_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))