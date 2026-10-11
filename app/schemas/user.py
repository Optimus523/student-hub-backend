from typing import Annotated
from pydantic import BaseModel, StringConstraints


class UserCreate(BaseModel):
    username: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=3,
            max_length=30,
            pattern=r"^[A-Za-z0-9_]+$",
            to_lower=True,
        ),
    ]
    password: Annotated[str, StringConstraints(min_length=8, max_length=128)]


class UserPublic(BaseModel):
    id: int
    username: str
