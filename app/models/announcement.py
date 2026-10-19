from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


# Represents a campus announcement stored in the database.
class Announcement(SQLModel, table=True):
    # Primary key for each announcement entry.
    id: int | None = Field(default=None, primary_key=True)

    # Short headline shown to users.
    title: str

    # Full content body for the announcement.
    body: str

    # Foreign key linking each announcement to its author user.
    author_id: int = Field(foreign_key="users.id")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
