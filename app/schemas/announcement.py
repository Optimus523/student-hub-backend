from pydantic import BaseModel


class AnnouncementIn(BaseModel):
    title: str
    body: str
