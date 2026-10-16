from pydantic import BaseModel


# Input payload expected when submitting a new announcement.
class AnnouncementIn(BaseModel):
    title: str
    body: str
