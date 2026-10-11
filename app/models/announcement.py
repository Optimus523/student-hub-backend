from sqlmodel import Field, SQLModel


class Announcement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    body: str
