from pydantic import BaseModel, Field
from datetime import datetime, timezone

class AssignmentIn(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    description: str = Field(min_length=5, max_length=2000)
    course_code: str = Field(min_length=3, max_length=20)
    due_date: datetime